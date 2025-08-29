from rest_framework import serializers
from .models import ErrandRequest, ErrandItem, Review


class ErrandItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrandItem
        fields = ['id', 'name', 'quantity', 'price', 'category']


class ErrandRequestCreateSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    category_input = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ErrandRequest
        fields = ['id', 'name', 'quantity', 'price', 'category', 'category_input']       

class ErrandRequestSerializer(serializers.ModelSerializer):
    items = ErrandItemSerializer(many=True, read_only=True)     
    requester_username = serializers.CharField(source='requester.username', read_only=True)
    runner_username = serializers.CharField(source='runner.username', read_only=True, allow_null=True)
    
    class Meta:
        model = ErrandRequest
        fields = ['id', 'title', 'description', 'status', 'requester', 'requester_username', 
                 'runner', 'runner_username', 'created_at', 'updated_at', 'items', 'reviews']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    reviewee_username = serializers.CharField(source='reviewee.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'errand', 'reviewer', 'reviewer_username', 'reviewee', 'reviewee_username', 
                 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'reviewee']  

class ErrandRequestSerializer(serializers.ModelSerializer):
    items = ErrandItemSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)  
    requester_username = serializers.CharField(source='requester.username', read_only=True)
    runner_username = serializers.CharField(source='runner.username', read_only=True, allow_null=True)
    
    class Meta:
        model = ErrandRequest
        fields = '__all__'