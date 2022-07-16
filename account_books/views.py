from django.db.models           import Q, Sum

from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from account_books.models       import AccountBook
from account_books.serializers  import AccountBookSerializer, AccountBookDetailSerializer, AccountBookCategorySerializer,\
                                       AccountBookCategoryDetailSerializer, AccountBookLogSerializer, AccountBookLogDetailSerializer,\
                                       AccountBookLogSchema

from account_books.models       import AccountBook, AccountBookCategory, AccountBookLog
from core.utils.get_obj         import GetAccountBook, GetAccountBookCategory, GetAccountBookLog
from core.utils.decorator       import query_debugger


class AccountBookView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    sort   = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern='?sort=', type=openapi.TYPE_STRING)
    search = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern='?search=', type=openapi.TYPE_STRING)
    status = openapi.Parameter('status', openapi.IN_QUERY, required=False, pattern='?status=', type=openapi.TYPE_STRING)
    offset = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit  = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    
    @query_debugger
    @swagger_auto_schema(responses={200: AccountBookSerializer}, manual_parameters=[sort, search, status, offset, limit])
    def get(self, request):
        user   = request.user
        
        search = request.GET.get('search', None)
        sort   = request.GET.get('sort', 'up_to_date')
        status = request.GET.get('status', 'deleted')
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))
            
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at',
            'high_budget': '-budget',
            'low_budget' : 'budget'
        }
            
        q = Q()
        
        if search:
            q |= Q(name__icontains = search)
        
        if user:
            q &= Q(users = user)
            
        books = AccountBook.objects\
                           .select_related('users')\
                           .filter(q)\
                           .exclude(status__iexact=status)\
                           .order_by(sort_set[sort])[offset:offset+limit]
                           
        serializer = AccountBookSerializer(books, many=True)
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=AccountBookSerializer, responses={201: AccountBookSerializer})
    def post(self, request):
        user = request.user
        
        serializer = AccountBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(users=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
        
class AccountBookDetailView(APIView):
    
    permission_classes = [IsAuthenticated]

    book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(
        request_body=AccountBookDetailSerializer, responses={200: AccountBookDetailSerializer},\
        manual_parameters=[book_id]
    )
    def patch(self, request, account_book_id):
        user = request.user
        
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookDetailSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(responses={200: '가계부가 삭제되었습니다.'}, manual_parameters=[book_id])
    def delete(self, request, account_book_id):
        user = request.user
        
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if book.status == 'deleted':
            return Response({'detail': f'가계부 {account_book_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        book.status = 'deleted'
        book.save()
        return Response({'detail': f'가계부 {account_book_id}(id)가 삭제되었습니다.'}, status=200)

        
class AccountBookRestoreView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={200: '가계부가 복구되었습니다.'}, manual_parameters=[book_id])
    def patch(self, request, account_book_id):
        user = request.user
        
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if book.status == 'in_use':
            return Response({'detail': f'가계부 {account_book_id}(id)는 이미 사용중입니다.'}, status=400)

        book.status = 'in_use'
        book.save()
        return Response({'detail': f'가계부 {account_book_id}(id)가 복구되었습니다.'}, status=200)
    

class AccountBookCategoryView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    sort   = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern='?sort=', type=openapi.TYPE_STRING)
    search = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern='?search=', type=openapi.TYPE_STRING)
    status = openapi.Parameter('status', openapi.IN_QUERY, required=False, pattern='?status=', type=openapi.TYPE_STRING)
    offset = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit  = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    
    @query_debugger
    @swagger_auto_schema(responses={200: AccountBookCategorySerializer}, manual_parameters=[sort, search, status, offset, limit])
    def get(self, request):
        user   = request.user
            
        search = request.GET.get('search', None)
        sort   = request.GET.get('sort', 'up_to_date')
        status = request.GET.get('status', 'deleted')
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))
            
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at'
        }
        
        q = Q()
        
        if search:
            q |= Q(name__icontains = search)
            
        if user:
            q &= Q(users = user)
            
        categories = AccountBookCategory.objects\
                                        .select_related('users')\
                                        .filter(q)\
                                        .exclude(status__iexact=status)\
                                        .order_by(sort_set[sort])[offset:offset+limit]
                                        
        serializer = AccountBookCategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=AccountBookCategorySerializer, responses={201: AccountBookCategorySerializer})
    def post(self, request):
        user = request.user
        
        serializer = AccountBookCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(users=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        

class AccountBookCategoryDetailView(APIView):
    
    permission_classes = [IsAuthenticated]

    account_book_category_id = openapi.Parameter('account_book_category_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        request_body=AccountBookCategoryDetailSerializer, responses={200: AccountBookCategoryDetailSerializer},\
        manual_parameters=[account_book_category_id]
    )
    def patch(self, request, account_book_category_id):
        user = request.user
        
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookCategoryDetailSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    account_book_category_id = openapi.Parameter('account_book_category_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(responses={200: '가계부 카테고리가 삭제되었습니다.'}, manual_parameters=[account_book_category_id])
    def delete(self, request, account_book_category_id):
        user = request.user
        
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if category.status == 'deleted':
            return Response({'detail': f'가계부 카테고리 {account_book_category_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        category.status = 'deleted'
        category.save()
        return Response({'detail': f'가계부 카테고리 {account_book_category_id}(id)가 삭제되었습니다.'}, status=200)


class AccountBookeCategoryRestoreView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    account_book_category_id = openapi.Parameter('account_book_category_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(responses={200: '가계부 카테고리가 복구되었습니다.'}, manual_parameters=[account_book_category_id])
    def patch(self, request, account_book_category_id):
        user = request.user
        
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if category.status == 'in_use':
            return Response({'detail': f'가계부 카테고리 {account_book_category_id}(id)는 이미 사용중입니다.'}, status=400)

        category.status = 'in_use'
        category.save()
        return Response({'detail': f'가계부 카테고리 {account_book_category_id}(id)가 복구되었습니다.'}, status=200)
    

class AccountBookLogView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    search     = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern='?search=', type=openapi.TYPE_STRING)
    sort       = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern='?sort=', type=openapi.TYPE_STRING)
    types      = openapi.Parameter('types', openapi.IN_QUERY, required=False, pattern='?types=', type=openapi.TYPE_STRING)
    categories = openapi.Parameter('categories', openapi.IN_QUERY, required=False, pattern='?categories=', type=openapi.TYPE_STRING)
    offset     = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit      = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    book_id    = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @query_debugger
    @swagger_auto_schema(
        responses={200: AccountBookLogSchema}, manual_parameters=[search, sort, types, categories, offset, limit, book_id]
    )    
    def get(self, request, account_book_id):
        user = request.user
            
        search        = request.GET.get('search', None)
        sort          = request.GET.get('sort', 'up_to_date')
        types         = request.GET.get('types', None) 
        categories_id = request.GET.getlist('categories', None)
        offset        = int(request.GET.get('offset', 0))
        limit         = int(request.GET.get('limit', 10))
        
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at',
            'high_price' : '-price',
            'low_price'  : 'price',    
        }
        
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        q = Q()
        
        if search:
            q |= Q(title__icontains = search)
            q |= Q(description__icontains = search)
            q |= Q(categories__name__icontains = search)
        
        if account_book_id:
            q &= Q(books_id = book.id)
        
        if categories_id:
            q &= Q(categories_id__in = categories_id)
            
        if types:
            q &= Q(types__iexact = types)
            
            
        logs = AccountBookLog.objects\
                             .select_related('categories', 'books')\
                             .filter(q)\
                             .order_by(sort_set[sort])
                             
        expenditure = logs.filter(types='expenditure').aggregate(total=Sum('price'))
        income      = logs.filter(types='income').aggregate(total=Sum('price'))
        
        data = {
            'nickname'         : user.nickname,
            'total_income'     : income['total'],
            'total_expenditure': expenditure['total'],
            'logs'             : (AccountBookLogSerializer(logs, many=True).data)[offset:offset+limit]
        }
        return Response(data, status=200)

    categories = openapi.Parameter('categories', openapi.IN_QUERY, required=True, pattern='?categories=', type=openapi.TYPE_STRING)
    book_id    = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(
        request_body=AccountBookLogSerializer, responses={200: AccountBookLogSerializer},\
        manual_parameters=[book_id, categories]
    )    
    def post(self, request, account_book_id):
        user = request.user
        
        account_book_category_id = request.GET.get('categories', None)
        
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(books=book, categories=category)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

class AccountBookLogDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    account_book_log_id = openapi.Parameter('account_book_log_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        request_body=AccountBookLogDetailSerializer, responses={200: AccountBookLogDetailSerializer},\
        manual_parameters=[account_book_log_id]
    )
    def patch(self, request, account_book_log_id):
        user = request.user
        
        log, err = GetAccountBookLog.get_log_n_check_error(account_book_log_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookLogDetailSerializer(log, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    account_book_log_id = openapi.Parameter('account_book_log_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(responses={200: '가계부 기록이 삭제되었습니다.'}, manual_parameters=[account_book_log_id])
    def delete(self, request, account_book_log_id):
        user = request.user
        
        log, err = GetAccountBookLog.get_log_n_check_error(account_book_log_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if log.status == 'deleted':
            return Response({'detail': f'가계부 기록 {account_book_log_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        log.status = 'deleted'
        log.save()
        return Response({'detail': f'가계부 기록 {account_book_log_id}(id)가 삭제되었습니다.'}, status=200)