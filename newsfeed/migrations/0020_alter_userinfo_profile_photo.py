# Generated by Django 4.2 on 2023-06-29 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0019_remove_photo_newsfeed_newsfeed_photos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='profile_photo',
            field=models.ImageField(upload_to='profile_photos/'),
        ),
    ]