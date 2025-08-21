from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

# Serializer for Django's built-in User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



# Serializer for Profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'full_name', 'phone', 'address',
            'user_type', 'bio', 'rating', 'is_available'
        ]


