from authentication.decorators import authenticate_user
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from appname.models.team import Team
import json

from django.db import transaction


@csrf_exempt
@authenticate_user
def team_views(request):
    if request.method == "GET":
        return team_index(request)
    elif request.method == "POST":
        return team_create(request)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@authenticate_user
def team_detail_views(request, pk):
    if request.method == "GET":
        return team_show(request, pk)
    elif request.method == "PUT" or request.method == "PATCH":
        return team_update(request, pk)
    elif request.method == "DELETE":
        return team_delete(request, pk)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def team_create(request):
    try:
        data = request.body and json.loads(request.body) or {}

        with transaction.atomic():
            team = Team.objects.create(**data)
            team.team_members.create(user_id=request.user["user_id"], role="owner")

        return JsonResponse(team_to_dict(team), status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def team_index(request):
    print("caiu aq")
    teams = Team.objects.filter(
        team_members__user_id=request.user["user_id"]
    ).distinct()

    teams_list = list(teams.values())
    return JsonResponse(teams_list, safe=False)


def team_show(request, pk):
    try:
        team = Team.objects.get(pk=pk, team_members__user_id=request.user["user_id"])
        return JsonResponse(team_to_dict(team))
    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)


def team_update(request, pk):
    try:
        task = Team.objects.get(pk=pk, team_members__user_id=request.user["user_id"])
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        return JsonResponse(team_to_dict(task))
    except Team.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)


def team_delete(request, pk):
    try:
        team = Team.objects.get(pk=pk, team_members__user_id=request.user["user_id"])
        team.delete()
        return HttpResponse(status=204)
    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)


def team_to_dict(team):
    return {
        "id": team.id,
        "created_at": team.created_at,
        "updated_at": team.updated_at,
    }
