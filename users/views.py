from rest_framework.views            import APIView
from rest_framework.permissions      import AllowAny, IsAuthenticated
from rest_framework.response         import Response
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken

from drf_yasg.utils    import swagger_auto_schema
from drf_yasg          import openapi

from users.serializers import UserSignUpSerializer, UserSignInSerializer, UserSignInSchema


class UserSignUpView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=UserSignUpSerializer, responses={201: UserSignUpSerializer})
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class UserSignInView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=UserSignInSerializer, responses={200: UserSignInSchema})
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        
        if serializer.is_valid():
            token = serializer.validated_data
            return Response(token, status=200)
        return Response(serializer.errors, status=400)
    

class UserSignOutView(APIView):
    permission_classes = [IsAuthenticated]
    
    post_params = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'refesh_token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    )
    @swagger_auto_schema(request_body=post_params, responses={200: '유저가 로그아웃 되었습니다.'})
    def post(self, request):
        user = request.user
        
        """
        해당 유저의 발급된 모든 리프레시 토큰을 사용 제한합니다.
        """
        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)
            
        return Response({'message' : f'유저 {user.nickname}이 로그아웃 되었습니다.'}, status=200)