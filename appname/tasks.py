from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User


@shared_task
def task_after_confirmed(task_id):
    from appname.models.tasks import Task

    task = Task.objects.get(pk=task_id)
    user = User.objects.get(pk=task.user_id)

    print(f"Sending email to {user.email}")
    print(f"Task {task.title} was completed!")
    print(f"Email sent from {settings.DEFAULT_FROM_EMAIL}")
    send_mail(
        "Tarefa concluída",
        f"Olá, a tarefa {task.title} foi concluída com sucesso!",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
