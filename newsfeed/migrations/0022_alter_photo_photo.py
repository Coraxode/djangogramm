# Generated by Django 4.2 on 2023-06-29 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0021_alter_newsfeed_photos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(max_length=255, upload_to='newsfeed_photos/'),
        ),
    ]
