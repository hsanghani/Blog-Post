from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import time
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

User = get_user_model()
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def create_jwt_pair_for_user(user):
    if user is None:
        raise ValueError("User cannot be None")

    refresh = RefreshToken.for_user(user)
    tokens = {
        "access": str(refresh.access_token), 
        "refresh": str(refresh), 
        # 'expires_at': time.time() + CACHE_TTL
        }
    return tokens
