# Generated by Django 5.0.6 on 2024-06-25 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appname', '0007_team_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('pending', 'PENDING'), ('accepted', 'ACCEPTED'), ('rejected', 'REJECTED')], default='pending', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_invitations', to='appname.team')),
            ],
        ),
    ]
