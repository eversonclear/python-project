import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        print(data["password"], data["email"])
        user = User.objects.filter(email=data["email"]).first()
        print("user", user is None)
        if user is None or not user.check_password(data["password"]):
            return JsonResponse({"error": "Invalid email or password"}, status=400)
        else:
            return JsonResponse(user_to_dict(user))
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if User.objects.filter(email=data["email"]).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        try:
            user = User.objects.create_user(
                username=data["email"],
                email=data["email"],
                password=data["password"],
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse(user_to_dict(user))
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def user_to_dict(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "token": generate_token(user.id),
    }


def generate_token(user_id):
    return jwt.encode({"user": user_id}, settings.SECRET_KEY, algorithm="HS256")
