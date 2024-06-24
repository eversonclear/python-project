from django.urls import include, path

urlpatterns = [
    path("", include("appname.urls.task")),
    path("", include("appname.urls.team")),
    path("", include("appname.urls.team_member")),
    path("", include("appname.urls.team_invitation")),
]
