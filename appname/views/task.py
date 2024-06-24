import json
from django.http import JsonResponse, HttpResponse
from appname.models.task import Task
from django.views.decorators.csrf import csrf_exempt
from authentication.decorators import authenticate_user


@csrf_exempt
@authenticate_user
def task_views(request):
    if request.method == "GET":
        return task_index(request)
    elif request.method == "POST":
        return task_create(request)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@authenticate_user
def task_detail_views(request, pk):
    if request.method == "GET":
        return task_show(request, pk)
    elif request.method == "PUT" or request.method == "PATCH":
        return task_update(request, pk)
    elif request.method == "DELETE":
        return task_delete(request, pk)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def task_index(request):
    if request.method == "GET":
        tasks = Task.objects.filter(user_id=request.user["user_id"])
        tasks_list = list(tasks.values())
        return JsonResponse(tasks_list, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def task_show(request, pk):
    try:
        task = Task.objects.get(pk=pk, user_id=request.user["user_id"])
        return JsonResponse(task_to_dict(task))
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)


def task_create(request):
    if request.method == "POST":
        data = json.loads(request.body)

        data["user_id"] = request.user["user_id"]
        task = Task.objects.create(**data)
        return JsonResponse(task_to_dict(task), status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def task_update(request, pk):
    try:
        task = Task.objects.get(pk=pk, user_id=request.user["user_id"])
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        return JsonResponse(task_to_dict(task))
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)


def task_delete(request, pk):
    try:
        task = Task.objects.get(pk=pk, user_id=request.user["user_id"])
        task.delete()
        return HttpResponse(status=204)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)


def task_to_dict(task):
    return {
        "id": task.id,
        "user_id": task.user_id,
        "title": task.title,
        "description": task.description,
        "complete": task.complete,
        "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
