from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.upload_video, name='upload_video'),
    path('watch/<int:video_id>/', views.video_player, name='video_player'),
    path('watch/<int:video_id>/save-position/', views.save_position, name='save_position'),
    path('watch/<int:video_id>/delete/', views.delete_video, name='delete_video'),
]