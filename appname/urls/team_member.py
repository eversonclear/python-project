from django.urls import path
from ..views.team_member import team_member_views, team_member_detail_views

urlpatterns = [
    path(
        "teams/<int:team_id>/team_members",
        team_member_views,
        name="team_member_views",
    ),
    path(
        "teams/<int:team_id>/team_members/<int:pk>",
        team_member_detail_views,
        name="team_member_detail_views",
    ),
]
