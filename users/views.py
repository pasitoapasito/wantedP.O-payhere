from rest_framework.views       import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response    import Response

from drf_yasg.utils    import swagger_auto_schema

from users.serializers import UserSignUpSerializer


class UserSignUpView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=UserSignUpSerializer, responses={201: UserSignUpSerializer})
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)