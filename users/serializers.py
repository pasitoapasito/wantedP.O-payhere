import re

from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSignUpSerializer(ModelSerializer):
    
    def create(self, validated_data):
        password = validated_data.get('password')
        
        """
        패스워드 정규식표현(길이 8~20 자리, 최소 1개 이상의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성)
        """
        password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'
        
        if not re.match(password_regex, password):
            raise serializers.ValidationError({'password': ['올바른 비밀번호를 입력하세요.']})
        
        """
        유저정보 DB에 저장
        """
        user = User.objects.create_user(**validated_data)
        return user
        
    class Meta:
        model        = User
        fields       = ['email', 'nickname', 'password']
        extra_kwargs = {'password': {'write_only': True}}