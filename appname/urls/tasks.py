from django.urls import path
from appname.views.tasks import task_views, task_detail_views

urlpatterns = [
    path("tasks", task_views, name="task_views"),
    path("tasks/<int:pk>", task_detail_views, name="task_detail_views"),
]
