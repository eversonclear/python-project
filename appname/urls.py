from django.urls import path
from .views import task_views, task_detail_views

urlpatterns = [
    path("tasks", task_views),
    path("tasks/<int:pk>", task_detail_views),
]
