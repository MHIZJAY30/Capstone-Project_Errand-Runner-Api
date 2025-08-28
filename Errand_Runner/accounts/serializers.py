from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    address = serializers.CharField(write_only=True, required=False, allow_blank=True)
    user_type = serializers.ChoiceField(write_only=True, choices=Profile.USER_TYPES, default='requester')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'phone', 'address', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        phone = validated_data.pop('phone', '')
        address = validated_data.pop('address', '')
        user_type = validated_data.pop('user_type', 'requester')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        Profile.objects.create(user=user, full_name=full_name, phone=phone, address=address, user_type=user_type)  
        return user

class ProfileSerializer(serializers.ModelSerializer): 
    user_type = serializers.ChoiceField(choices=Profile.USER_TYPES)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'phone', 'address', 'user_type', 'bio', 'rating', 'is_available']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


