from django.urls import path
from ..views.team_invitation import (
    team_invitations_views,
    team_invitation_accepted_view,
)

urlpatterns = [
    path(
        "teams/<int:team_id>/team_invitations",
        team_invitations_views,
        name="team_invitations_views",
    ),
    path(
        "team_invitations/<str:invitation_token>/accept",
        team_invitation_accepted_view,
        name="team_invitation_accepted_view",
    ),
]
