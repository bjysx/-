from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'avatar', 'phone', 'role', 'email', 'department', 'position')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Save current token to user model
        # Note: We save the token without the 'Bearer ' prefix
        # because the frontend will add it when sending requests
        self.user.current_token = data['access']
        self.user.save()
        data['user'] = UserSerializer(self.user).data
        return data
