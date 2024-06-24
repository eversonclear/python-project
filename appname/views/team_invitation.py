from appname.models.team import Team
from appname.models.team_invitation import TeamInvitation, Status
from appname.models.team_member import TeamMember, Role
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.decorators import authenticate_user
from django.conf import settings

from django.contrib.auth.models import User

from django.db import transaction

import json
import jwt


@csrf_exempt
@authenticate_user
def team_invitations_views(request, team_id):
    try:
        team = Team.objects.get(
            pk=team_id, team_members__user_id=request.user["user_id"]
        )
    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)

    if request.method == "POST":
        return team_invitation_create(request, team)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def team_invitation_accepted_view(request, invitation_token):
    token_data = jwt.decode(invitation_token, settings.SECRET_KEY, algorithms=["HS256"])

    try:
        with transaction.atomic():
            if User.exists(email=token_data["email"]):
                user = User.objects.get(email=token_data["email"])
            else:
                user = User.objects.create(email=token_data["email"])

            team = Team.objects.get(pk=token_data["team_id"])
            team.team_members.create(user=user, role="MEMBER")

            team_invitation = TeamInvitation.objects.get(pk=token_data["invitation_id"])
            team_invitation.status = "ACCEPTED"
            team_invitation.save()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def team_invitation_create(request, team):
    try:
        data = request.body and json.loads(request.body) or {}
        email = data.get("email")

        current_team_member = team.team_members.get(
            user_id=request.user["user_id"], role=Role.ADMIN.value
        )

        team_invitation = team.team_invitations.create(
            email=email,
            team=team,
            token=generate_invitation_token(
                current_team_member.team_id, email, team_invitation.id
            ),
        )

        return JsonResponse(team_invitation_to_dict(team_invitation), status=201)
    except TeamMember.DoesNotExist:
        return JsonResponse(
            {"error": "Only admin can create team invitation"}, status=403
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def team_invitation_to_dict(team_invitation):
    return {
        "id": team_invitation.id,
        "email": team_invitation.email,
        "team_id": team_invitation.team_id,
        "token": team_invitation.token,
        "created_at": team_invitation.created_at,
        "updated_at": team_invitation.updated_at,
    }


def generate_invitation_token(team_id, email, invitation_id):
    jwt.encode(
        {"team_id": team_id, "email": email, "invitation_id": invitation_id},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
