from django.db import models

from .team import Team
from django.contrib.auth.models import User

from enum import Enum

from django.core.exceptions import ValidationError


class Role(Enum):
    ADMIN = "admin"
    MEMBER = "member"


def validate_team(value):
    if not value:
        raise ValidationError("Team cannot be blank.")
    if not Team.objects.filter(id=value).exists():
        raise ValidationError("Team does not exist.")


def validate_user(value):
    if not value:
        raise ValidationError("User cannot be blank.")
    if not User.objects.filter(id=value).exists():
        raise ValidationError("User does not exist.")


class TeamMember(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="team_members",
        validators=[validate_team],
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, validators=[validate_user])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(
        max_length=6,
        choices=[(tag.value, tag.name) for tag in Role],
        default=Role.MEMBER.value,
    )
