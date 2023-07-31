from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from django.urls import path

from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all_posts/', views.all_posts, name='all_posts'),
    path('user/settings/<str:username>/', login_required(views.user_settings), name='user_settings'),
    path('user/<str:username>/', login_required(views.user_profile), name='user_profile'),
    path('like_photo/', login_required(views.like_photo), name='like_photo'),
    path('change_tags/', login_required(views.change_tags), name='change_tags'),
    path('upload/', login_required(views.upload), name='upload'),
    path('subscribe/', login_required(views.subscribe), name='subscribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
