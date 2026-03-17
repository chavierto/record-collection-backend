import jwt
from django.http import JsonResponse
from django.conf import settings

_jwks_client = None


def _get_jwks_client():
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = jwt.PyJWKClient(settings.CLERK_JWKS_URL)
    return _jwks_client


class ClerkAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'detail': 'Authentication required.'}, status=401)

        token = auth_header[7:]
        try:
            client = _get_jwks_client()
            signing_key = client.get_signing_key_from_jwt(token)
            payload = jwt.decode(token, signing_key.key, algorithms=['RS256'])
            request.user_id = payload['sub']
        except Exception:
            return JsonResponse({'detail': 'Invalid or expired token.'}, status=401)

        return self.get_response(request)
