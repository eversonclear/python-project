from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ..tasks import task_after_confirmed
from django.core.exceptions import ValidationError


def validate_title(value):
    print("validate_title", value)
    if not value:
        raise ValidationError("Title cannot be blank.")


def validate_description(value):
    if not value:
        raise ValidationError("Description cannot be blank.")
    if len(value) < 5:
        raise ValidationError("Description must be at least 5 characters.")


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[validate_title])
    description = models.CharField(max_length=500, validators=[validate_description])
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(pre_save, sender=Task)
def before_task_save_handler(sender, instance, *args, **kwargs):
    original_complete = None
    if instance.id:
        original_complete = Task.objects.get(pk=instance.id).complete

    instance.__original_complete = original_complete


@receiver(post_save, sender=Task)
def task_confirmed_handler(sender, instance, **kwargs):
    if instance.complete and instance.__original_complete is False:
        task_after_confirmed.delay(instance.id)
