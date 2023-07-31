from django.contrib import admin
from .models import Newsfeed, UserInfo, Tags, Photo


admin.site.register(Newsfeed)
admin.site.register(UserInfo)
admin.site.register(Tags)
admin.site.register(Photo)
