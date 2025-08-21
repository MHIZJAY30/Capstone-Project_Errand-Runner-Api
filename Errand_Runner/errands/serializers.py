from rest_framework import serializers
from .models import ErrandRequest, ErrandItem


class ErrandItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrandItem
        fields = ['id', 'name', 'quantity', 'price', 'category']


class ErrandRequestSerializer(serializers.ModelSerializer):
    items = ErrandItemSerializer(many=True, read_only=True)  # Nested items
    requester_username = serializers.StringRelatedField(source='requester.username', read_only=True)  # Show username
    runner_username = serializers.StringRelatedField(ource='runner.username', read_only=True, allow_null=True)

    class Meta:
        model = ErrandRequest
        fields = [
            'id', 'user', 'runner', 'title', 'description', 'pickup_location',
            'dropoff_location', 'status', 'created_at', 'updated_at',
            'deadline', 'runner_confirmed', 'items'
        ]


class ErrandRequestCreateSerializer(serializers.ModelSerializer):
    """For creating errands along with items"""
    items = ErrandItemSerializer(many=True, required=False)

    class Meta:
        model = ErrandRequest
        fields = [
            'title', 'description', 'pickup_location', 'dropoff_location',
            'deadline', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        user = self.context['request'].user
        errand = ErrandRequest.objects.create(user=user, **validated_data)

        # Create items if provided
        for item_data in items_data:
            ErrandItem.objects.create(errand=errand, **item_data)
        return errand

