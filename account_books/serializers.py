from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer

from account_books.models       import AccountBook, AccountBookCategory, AccountBookLog


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
        
        instance.name = validated_data.get('name', instance.name)
        
        instance.save()
        return instance
    
    class Meta:
        model  = AccountBookCategory
        fields = ['id', 'nickname', 'name', 'status']
        extra_kwargs = {
            'id': {'read_only': True}
        }
        
        
class AccountBookLogSerializer(ModelSerializer):
    category    = serializers.SerializerMethodField()
    book        = serializers.SerializerMethodField()
    created_at  = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    price       = serializers.DecimalField(max_digits=10, decimal_places=0)
    
    def get_category(self, obj):
        if obj.categories.status == 'deleted':
            category = None
        category = obj.categories.name
        return category
    
    def get_book(self, obj):
        return obj.books.name
    
    def get_created_at(self, obj):
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
    def get_modified_at(self, obj):
        return (obj.modified_at).strftime('%Y-%m-%d %H:%M')
    
    def create(self, validated_data):
        log = AccountBookLog.objects.create(**validated_data)
        return log
    
    class Meta:
        model  = AccountBookLog
        fields = [
            'id', 'title', 'types', 'price', 'description', 'status',\
            'category', 'book', 'created_at', 'modified_at'
        ]
        extra_kwargs = {
            'id': {'read_only': True}
        }


class AccountBookLogDetailSerializer(ModelSerializer):
    category    = serializers.SerializerMethodField()
    book        = serializers.SerializerMethodField()
    created_at  = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    price       = serializers.DecimalField(max_digits=10, decimal_places=0)
    
    def get_category(self, obj):
        if obj.categories.status == 'deleted':
            category = None
        category = obj.categories.name
        return category
    
    def get_book(self, obj):
        return obj.books.name
    
    def get_created_at(self, obj):
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
    def get_modified_at(self, obj):
        return (obj.modified_at).strftime('%Y-%m-%d %H:%M')
    
    def update(self, instance, validated_data):
        
        instance.title       = validated_data.get('title', instance.title)
        instance.types       = validated_data.get('types', instance.types)
        instance.price       = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        
        instance.save()
        return instance
    
    class Meta:
        model  = AccountBookLog
        fields = [
            'id', 'title', 'types', 'price', 'description', 'status',\
            'category', 'book', 'created_at', 'modified_at'
        ]
        extra_kwargs = {
            'id'      : {'read_only': True},
            'book'    : {'read_only': True},
            'category': {'read_only': True},
        }


class AccountBookLogSchema(serializers.Serializer):
    nickname          = serializers.CharField(max_length=100)
    total_income      = serializers.DecimalField(max_digits=10, decimal_places=0)
    total_expenditure = serializers.DecimalField(max_digits=10, decimal_places=0)
    logs              = AccountBookLogSerializer(many=True)