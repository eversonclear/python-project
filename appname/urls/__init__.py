from django.urls import include, path

urlpatterns = [
    path("", include("appname.urls.task")),
]
