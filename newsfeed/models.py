from django.db import models
from django.contrib.auth.models import User


class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Photo(models.Model):
    photo = models.ImageField(upload_to='newsfeed_photos/', unique=False, max_length=255)

    def __str__(self):
        return f"{str(self.photo).split('/')[1]}"


class Newsfeed(models.Model):
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    photos = models.ManyToManyField(Photo, blank=False)
    likes = models.ManyToManyField(User, related_name='N_likes', blank=True)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return f"{self.user}'s photos"


class UserInfo(models.Model):
    profile_photo = models.ImageField(upload_to='profile_photos/', unique=False)
    biography = models.TextField(blank=True)
    subscriptions = models.ManyToManyField(User, related_name='subscriptions', blank=True)

    def __str__(self):
        try:
            return f"Info about {User.objects.get(id=self.id).username}"
        except IndexError:
            return "can't find user"
