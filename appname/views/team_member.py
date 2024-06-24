from authentication.decorators import authenticate_user
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from appname.models.team import Team
import json

from appname.models.team_member import Role


@csrf_exempt
@authenticate_user
def team_member_views(request, team_id):
    try:
        team = Team.objects.get(
            pk=team_id, team_members__user_id=request.user["user_id"]
        )
    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)

    if request.method == "GET":
        return team_member_index(request, team)
    elif request.method == "POST":
        return team_member_create(request, team)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@authenticate_user
def team_member_detail_views(request, pk, team_id):
    try:
        team = Team.objects.get(
            pk=team_id, team_members__user_id=request.user["user_id"]
        )
    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)

    if request.method == "GET":
        return team_member_show(request, team, pk)
    elif request.method == "PUT" or request.method == "PATCH":
        return team_member_update(request, team, pk)
    elif request.method == "DELETE":
        return team_member_delete(request, team, pk)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def team_member_create(request, team):
    try:
        data = request.body and json.loads(request.body) or {}
        current_team_member = team.team_members.filter(
            user_id=data.get("user_id")
        ).first()

        if current_team_member.role != Role.ADMIN.value:
            return JsonResponse({"error": "Only admin can add team member"}, status=403)

        team_member = team.team_members.create(**data)

        return JsonResponse(team_member_to_dict(team_member), status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def team_member_index(request, team):
    team_members = team.team_members.all()

    team_members_list = list(team_members.values())
    team_members_list = [team_member_to_dict(tm) for tm in team_members]

    return JsonResponse(team_members_list, safe=False)


def team_member_show(request, team, pk):
    try:
        team_member = team.team_members.get(pk=pk)
        return JsonResponse(team_member_to_dict(team_member))
    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)


def team_member_update(request, team, pk):
    try:
        team_member = team.team_members.get(pk=pk)
        data = json.loads(request.body)
        for key, value in data.items():
            if key == "role" and value == Role.ADMIN.value:
                if team_member.role != Role.ADMIN.value:
                    return JsonResponse(
                        {"error": "Only admin can update role to admin"}, status=403
                    )

            setattr(team_member, key, value)

        team_member.save()
        return JsonResponse(team_member_to_dict(team_member))
    except Team.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)


def team_member_delete(request, team, pk):
    try:
        team_member = team.team_members.get(pk=pk)

        if team_member.role != Role.ADMIN.value:
            return JsonResponse(
                {"error": "Only admin can delete team member"}, status=403
            )

        team_member.delete()
        return HttpResponse(status=204)
    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)


def team_member_to_dict(team_member):
    return {
        "id": team_member.id,
        "team_id": team_member.team_id,
        "user": {
            "id": team_member.user.id,
            "email": team_member.user.email,
        },
        "role": team_member.role,
        "created_at": team_member.created_at,
        "updated_at": team_member.updated_at,
    }
