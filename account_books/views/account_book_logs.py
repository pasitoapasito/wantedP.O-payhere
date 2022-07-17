from django.db.models           import Q, Sum

from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from account_books.models       import AccountBookLog
from account_books.serializers  import AccountBookLogSerializer, AccountBookLogDetailSerializer,\
                                       AccountBookLogSchema

from core.utils.get_obj         import GetAccountBook, GetAccountBookCategory, GetAccountBookLog
from core.utils.decorator       import query_debugger


class AccountBookLogView(APIView):
    """
    Assignee: 김동규
    
    query string: sort, search, types, categories, offset, limit
    query param: account_book_id
    return: json
    detail:
      - 인증/인가에 통과한 유저는 본인의 가계부 기록 리스트 정보를 호출할 수 있습니다.(GET: 가계부 기록 조회 기능)
        > 부가기능
          * 가계부 기록 검색기능
          * 정렬 기능(생성일자, 금액을 기준으로 정렬)
          * 가계부 필터링 기능(카테고리/타입)
          * 페이지네이션 기능(원하는 크기의 데이터 개수를 호출)
      - 인증/인가에 통과한 유저가 가계부 기록을 생성할 수 있습니다.(POST: 가계부 기록 생성 기능)
    """
    
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
        """
        가계부 기록 조회(리스트) 기능
        """
        user = request.user
            
        search        = request.GET.get('search', None)
        sort          = request.GET.get('sort', 'up_to_date')
        types         = request.GET.get('types', None) 
        categories_id = request.GET.getlist('categories', None)
        offset        = int(request.GET.get('offset', 0))
        limit         = int(request.GET.get('limit', 10))
        
        """
        정렬 기준
        """ 
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at',
            'high_price' : '-price',
            'low_price'  : 'price',    
        }
        
        """
        가계부의 존재여부 및 유저정보 확인
        """
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        q = Q()
        
        """
        검색 기능
        """
        if search:
            q |= Q(title__icontains = search)
            q |= Q(description__icontains = search)
            q |= Q(categories__name__icontains = search)
        
        """
        본인의 가계부 기록 정보 호출
        """
        if account_book_id:
            q &= Q(books_id = book.id)
        
        """
        카테고리 필터링 기능
        """
        if categories_id:
            q &= Q(categories_id__in = categories_id)
        
        """
        타입 필터링 기능
        """    
        if types:
            q &= Q(types__iexact = types)
            
        logs = AccountBookLog.objects\
                             .select_related('categories', 'books')\
                             .filter(q)\
                             .order_by(sort_set[sort])                    
        """
        총지출/총수입 기록 산출
        """                 
        expenditure = logs.filter(types='expenditure').aggregate(total=Sum('price'))
        income      = logs.filter(types='income').aggregate(total=Sum('price'))
        
        """
        가계부 기록 종합 데이터(페이지네이션 기능 포함)
        """
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
        """
        가계부 기록 생성 기능
        """
        user = request.user
        
        """
        가계부 카테고리 정보(필수값)
        """
        account_book_category_id = request.GET.get('categories', None)
        
        """
        가계부의 존재여부 및 유저정보 확인
        """
        book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        """
        가계부 카테고리의 존재여부 및 유저정보 확인
        """
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(books=book, categories=category)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

class AccountBookLogDetailView(APIView):
    """
    Assignee: 김동규
    
    query param: account_book_log_id
    return: json
    detail:
      - 인증/인가에 통과한 유저는 본인의 가계부 기록을 수정할 수 있습니다.(PATCH: 가계부 기록 수정 기능)
      - 인증/인가에 통과한 유저는 본인의 가계부 기록을 삭제할 수 있습니다.(DELETE: 가계부 기록 삭제 기능)
    """
    
    permission_classes = [IsAuthenticated]
    
    log_id = openapi.Parameter('account_book_log_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        request_body=AccountBookLogDetailSerializer, responses={200: AccountBookLogDetailSerializer},\
        manual_parameters=[log_id]
    )
    def patch(self, request, account_book_log_id):
        """
        가계부 기록 수정 기능(가계부 기록 제목/타입/금액/설명 수정)
        """
        user = request.user
        
        """
        가계부 기록의 존재여부 및 유저정보 확인
        """
        log, err = GetAccountBookLog.get_log_n_check_error(account_book_log_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookLogDetailSerializer(log, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    log_id = openapi.Parameter('account_book_log_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(responses={200: '가계부 기록이 삭제되었습니다.'}, manual_parameters=[log_id])
    def delete(self, request, account_book_log_id):
        """
        가계부 기록 삭제 기능
        """
        user = request.user
        
        """
        가계부 기록의 존재여부 및 유저정보 확인
        """
        log, err = GetAccountBookLog.get_log_n_check_error(account_book_log_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if log.status == 'deleted':
            return Response({'detail': f'가계부 기록 {account_book_log_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        log.status = 'deleted'
        log.save()
        return Response({'detail': f'가계부 기록 {account_book_log_id}(id)가 삭제되었습니다.'}, status=200)