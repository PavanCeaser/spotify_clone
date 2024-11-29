from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    # urls.py
    path('play-track/', views.play_track, name='play_track'),
    path('playlist/create/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('add-to-playlist/<int:song_id>/<int:playlist_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('remove-from-playlist/<int:playlist_id>/<int:song_id>/', views.remove_from_playlist, name='remove_from_playlist'),
]