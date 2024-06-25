from django.core.management.base import BaseCommand
from appname.models.task import Task
from appname.elasticsearch_client import index_task


class Command(BaseCommand):
    help = "Reindex all tasks in Elasticsearch"

    def handle(self, *args, **kwargs):
        tasks = Task.objects.all()
        for task in tasks:
            index_task(task)
        self.stdout.write(self.style.SUCCESS("Successfully reindexed all tasks"))
