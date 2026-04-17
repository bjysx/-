from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that checks if the token is the current token for the user
    """
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        user_id = validated_token.get('user_id')
        if user_id is None:
            raise AuthenticationFailed('No user id in token')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        
        # Check if the token is the current token for the user
        if not user.current_token:
            raise AuthenticationFailed('Token has been invalidated')
        
        return user
