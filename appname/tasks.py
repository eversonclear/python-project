from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User


@shared_task
def task_after_confirmed(task_id):
    from appname.models.task import Task

    task = Task.objects.get(pk=task_id)
    user = User.objects.get(pk=task.user_id)

    send_mail(
        "Tarefa concluída",
        f"Olá, a tarefa {task.title} foi concluída com sucesso!",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


@shared_task
def send_invitation_email(invitation_id):
    from appname.models.team_invitation import TeamInvitation

    invitation = TeamInvitation.objects.get(pk=invitation_id)

    send_mail(
        "Convite para o time",
        f"Olá, você foi convidado para o time {invitation.team.name}. Acesse o link para aceitar o convite: http://localhost:3000/team_invitations/{invitation.token}/accept",
        settings.DEFAULT_FROM_EMAIL,
        [invitation.email],
    )
