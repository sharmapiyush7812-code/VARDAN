import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta


class JWTAuthentication(BaseAuthentication):
    """Custom JWT authentication using PyJWT."""
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header[7:]  # Remove 'Bearer ' prefix
        
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return (None, token)  # Return user data (None in this MVP), token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
    
    @staticmethod
    def generate_token(user_id):
        """Generate a JWT token for a user."""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
    
    @staticmethod
    def decode_token(token):
        """Decode a JWT token and return the payload."""
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def get_user_from_token(request):
        """Extract user_id from JWT token in request."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header[7:]
        payload = JWTAuthentication.decode_token(token)
        return payload.get('user_id') if payload else None
