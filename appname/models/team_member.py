from django.db import models

from .team import Team
from django.contrib.auth.models import User

from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    MEMBER = "member"


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(
        max_length=6,
        choices=[(tag.value, tag.name) for tag in Role],
        default=Role.MEMBER.value,
    )
