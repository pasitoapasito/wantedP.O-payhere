from django.db.models           import Q

from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from account_books.models       import AccountBookCategory
from account_books.serializers  import AccountBookCategorySerializer, AccountBookCategoryDetailSerializer

from core.utils.get_obj         import GetAccountBookCategory
from core.utils.decorator       import query_debugger


class AccountBookCategoryView(APIView):
    """
    Assignee: 김동규
    
    query string: sort, search, status, offset, limit
    return: json
    detail:
      - 인증/인가에 통과한 유저는 본인의 가계부 카테고리 리스트 정보를 호출할 수 있습니다.(GET: 가계부 카테고리 조회 기능)
        > 부가기능
          * 가계부 카테고리 검색기능
          * 정렬 기능(생성일자 기준으로 정렬)
          * 가계부 카테고리 필터링 기능(사용중인 가계부/삭제된 가계부)
          * 페이지네이션 기능(원하는 크기의 데이터 개수를 호출)
      - 인증/인가에 통과한 유저가 가계부 카테고리를 생성할 수 있습니다.(POST: 가계부 카테고리 생성 기능)
    """
    
    permission_classes = [IsAuthenticated]
    
    sort   = openapi.Parameter('sort', openapi.IN_QUERY, required=False, pattern='?sort=', type=openapi.TYPE_STRING)
    search = openapi.Parameter('search', openapi.IN_QUERY, required=False, pattern='?search=', type=openapi.TYPE_STRING)
    status = openapi.Parameter('status', openapi.IN_QUERY, required=False, pattern='?status=', type=openapi.TYPE_STRING)
    offset = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit  = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    
    @query_debugger
    @swagger_auto_schema(responses={200: AccountBookCategorySerializer}, manual_parameters=[sort, search, status, offset, limit])
    def get(self, request):
        """
        가계부 카테고리 조회(리스트) 기능
        """
        user = request.user
            
        search = request.GET.get('search', None)
        sort   = request.GET.get('sort', 'up_to_date')
        status = request.GET.get('status', 'deleted')
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))
        
        """
        정렬 기준
        """
        sort_set = {
            'up_to_date' : '-created_at',
            'out_of_date': 'created_at'
        }
        
        q = Q()
        
        """
        검색 기능
        """
        if search:
            q |= Q(name__icontains = search)
        
        """
        본인의 가계부 카테고리 정보 호출
        """
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
        """
        가계부 카테고리 생성 기능
        """
        user = request.user
        
        serializer = AccountBookCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(users=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        

class AccountBookCategoryDetailView(APIView):
    """
    Assignee: 김동규
    
    query param: account_book_category_id
    return: json
    detail:
      - 인증/인가에 통과한 유저는 본인의 가계부 카테고리를 수정할 수 있습니다.(PATCH: 가계부 카테고리 수정 기능)
      - 인증/인가에 통과한 유저는 본인의 가계부 카테고리를 삭제할 수 있습니다.(DELETE: 가계부 카테고리 삭제 기능)
    """
    
    permission_classes = [IsAuthenticated]

    category_id = openapi.Parameter('account_book_category_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        request_body=AccountBookCategoryDetailSerializer, responses={200: AccountBookCategoryDetailSerializer},\
        manual_parameters=[category_id]
    )
    def patch(self, request, account_book_category_id):
        """
        가계부 카테고리 수정 기능(가계부 카테고리 이름 수정)
        """
        user = request.user
        
        """
        가계부 카테고리의 존재여부 및 유저정보 확인
        """
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = AccountBookCategoryDetailSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    category_id = openapi.Parameter('account_book_category_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(responses={200: '가계부 카테고리가 삭제되었습니다.'}, manual_parameters=[category_id])
    def delete(self, request, account_book_category_id):
        """
        가계부 카테고리 삭제 기능
        """
        user = request.user
        
        """
        가계부 카테고리의 존재여부 및 유저정보 확인
        """
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if category.status == 'deleted':
            return Response({'detail': f'가계부 카테고리 {account_book_category_id}(id)는 이미 삭제된 상태입니다.'}, status=400)
        
        category.status = 'deleted'
        category.save()
        return Response({'detail': f'가계부 카테고리 {account_book_category_id}(id)가 삭제되었습니다.'}, status=200)


class AccountBookeCategoryRestoreView(APIView):
    """
    Assignee: 김동규
    
    query param: account_book_category_id
    return: json
    detail: 인증/인가에 통과한 유저는 본인의 삭제된 가계부 카테고리를 복구할 수 있습니다.(PATCH: 가계부 카테고리 복구 기능)
    """
    
    permission_classes = [IsAuthenticated]
    
    category_id = openapi.Parameter('account_book_category_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(responses={200: '가계부 카테고리가 복구되었습니다.'}, manual_parameters=[category_id])
    def patch(self, request, account_book_category_id):
        """
        가계부 카테고리 복구 기능
        """
        user = request.user
        
        """
        가계부 카테고리의 존재여부 및 유저정보 확인
        """
        category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        if category.status == 'in_use':
            return Response({'detail': f'가계부 카테고리 {account_book_category_id}(id)는 이미 사용중입니다.'}, status=400)

        category.status = 'in_use'
        category.save()
        return Response({'detail': f'가계부 카테고리 {account_book_category_id}(id)가 복구되었습니다.'}, status=200)