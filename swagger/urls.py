from django.urls import path
from .views import swagger_json, swagger_ui

urlpatterns = [
    path("swagger/", swagger_ui),
    path("swagger_json/", swagger_json, name="swagger_json"),
]
