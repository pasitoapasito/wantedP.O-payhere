from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from account_books.models       import AccountBook, AccountBookCategory


class AccountBookSerializer(ModelSerializer):
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj):
        return obj.users.nickname
    
    def create(self, validated_data):
        book = AccountBook.objects.create(**validated_data)
        return book
            
    class Meta:
        model  = AccountBook
        fields = ['id', 'nickname', 'name', 'budget', 'status']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class AccountBookDetailSerializer(ModelSerializer):
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj):
        return obj.users.nickname
    
    def update(self, instance, validated_data):
        
        instance.name   = validated_data.get('name', instance.name)
        instance.budget = validated_data.get('budget', instance.budget)
        instance.status = validated_data.get('status', instance.status)
        
        instance.save()
        return instance
    
    class Meta:
        model  = AccountBook
        fields = ['id', 'nickname', 'name', 'budget', 'status']
        extra_kwargs = {
            'id': {'read_only': True}
        }
        
        
class AccountBookCategorySerializer(ModelSerializer):
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj):
        return obj.users.nickname
    
    def create(self, validated_data):
        category = AccountBookCategory.objects.create(**validated_data)
        return category
    
    class Meta:
        model  = AccountBookCategory
        fields = ['id', 'nickname', 'name', 'status']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class AccountBookCategoryDetailSerializer(ModelSerializer):
    nickname = serializers.SerializerMethodField()
    
    def get_nickname(self, obj):
        return obj.users.nickname
    
    def update(self, instance, validated_data):
        
        instance.name   = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        
        instance.save()
        return instance
    
    class Meta:
        model  = AccountBookCategory
        fields = ['id', 'nickname', 'name', 'status']
        extra_kwargs = {
            'id': {'read_only': True}
        }