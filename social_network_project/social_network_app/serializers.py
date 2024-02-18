from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequest, Friendship

# User Serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'id']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

    def authenticate(self, email, password):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

# user = CustomUser.objects.get(email= "dip@gmail.com", password= "dipghosh099")


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'