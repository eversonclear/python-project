from django.db import models
from .team import Team

from enum import Enum

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..tasks import send_invitation_email

from django.core.exceptions import ValidationError


def validate_team(value):
    if not value:
        raise ValidationError("Team cannot be blank.")
    if not Team.objects.filter(id=value).exists():
        raise ValidationError("Team does not exist.")


def validate_email(value):
    if not value:
        raise ValidationError("Email cannot be blank.")


class Status(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class TeamInvitation(models.Model):
    email = models.EmailField(validators=[validate_email])
    token = models.CharField(max_length=255, null=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="team_invitations",
        validators=[validate_team],
    )
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
