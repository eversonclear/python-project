from django.urls import path
from ..views.team import team_views, team_detail_views

urlpatterns = [
    path("teams", team_views, name="team_views"),
    path("teams/<int:pk>", team_detail_views, name="team_detail_views"),
]
