# Generated by Django 4.2 on 2023-04-29 12:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsfeed', '0015_alter_userinfo_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsfeed',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='newsfeed',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='N_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='biography',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='profile_photo',
            field=models.TextField(blank=True),
        ),
    ]
