# myapp/decorators.py
import jwt
from django.http import JsonResponse
from functools import wraps

from django.conf import settings


def authenticate_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if auth_header is None:
            return JsonResponse({"error": "Authorization header missing"}, status=401)

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return JsonResponse(
                {"error": "Invalid authorization header format"}, status=401
            )

        token = parts[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
