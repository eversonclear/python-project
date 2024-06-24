from django.db import models
from .team import Team

from enum import Enum

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..tasks import send_invitation_email


class Status(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class TeamInvitation(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8,
        choices=[(tag.value, tag.name) for tag in Status],
        default=Status.PENDING.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=TeamInvitation)
def team_invitation_post_save_handler(sender, instance, created, **kwargs):
    if created:
        send_invitation_email.delay(instance.id)
