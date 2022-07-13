from django.db.models           import Q

from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from account_books.models       import AccountBook
from account_books.serializers  import AccountBookSerializer, AccountBookDetailSerializer

from account_books.models       import AccountBook
from core.utils                 import GetAccountBook

class AccountBookView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    sort   = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern="?sort=", type=openapi.TYPE_STRING)
    search = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern="?search=", type=openapi.TYPE_STRING)
    status = openapi.Parameter('status', openapi.IN_QUERY, required=False, pattern="?status=", type=openapi.TYPE_STRING)
    offset = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern="?offset=", type=openapi.TYPE_STRING)
    limit  = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern="?limit=", type=openapi.TYPE_STRING)
    
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
        
        if user:
            q &= Q(users=user)
        
        if search:
            q |= Q(name__icontains = search)
            
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

    account_book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(request_body=AccountBookDetailSerializer, responses={200: AccountBookDetailSerializer}, manual_parameters=[account_book_id])
    def patch(self, request, account_book_id):
        user = request.user
        
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({"detail" : err}, status=400)
        
        serializer = AccountBookDetailSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    account_book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={200: '가계부가 성공적으로 삭제되었습니다.'}, manual_parameters=[account_book_id])
    def delete(self, request, account_book_id):
        user = request.user
        
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({"detail" : err}, status=400)
        
        if book.status == 'deleted':
            return Response({'detail': f'가계부 {account_book_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        book.status = 'deleted'
        book.save()
        return Response({'detail': f'가계부 {account_book_id}(id)가 삭제되었습니다.'}, status=200)

        
class AccountBookRestoreView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    account_book_id = openapi.Parameter('account_book_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(responses={200: '가계부가 성공적으로 복구되었습니다.'}, manual_parameters=[account_book_id])
    def patch(self, request, account_book_id):
        user = request.user
        
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({"detail" : err}, status=400)
        
        if book.status == 'in_use':
            return Response({'detail': f'가계부 {account_book_id}(id)는 이미 사용중입니다.'}, status=400)

        book.status = 'in_use'
        book.save()
        return Response({'detail': f'가계부 {account_book_id}(id)가 복구되었습니다.'}, status=200)