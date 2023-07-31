# Generated by Django 4.1.7 on 2023-02-21 18:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsfeed', '0007_likesphotos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='newsfeed',
            name='likes',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='LikesPhotos',
        ),
        migrations.AddField(
            model_name='newsfeed',
            name='tags',
            field=models.ManyToManyField(to='newsfeed.tags'),
        ),
    ]