from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Album, Playlist, Song

class HomeView(ListView):
    model = Album
    template_name = 'music/index.html'
    context_object_name = 'albums'
    ordering = ['-release_date']
    paginate_by = 12

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'music/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = self.object.songs.all()
        return context

class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'music/playlist_detail.html'
    context_object_name = 'playlist'

@login_required
def create_playlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        is_public = request.POST.get('is_public', False) == 'on'
        playlist = Playlist.objects.create(
            name=name,
            user=request.user,
            is_public=is_public
        )
        messages.success(request, f'Playlist "{name}" created successfully!')
        return redirect('music:playlist_detail', pk=playlist.pk)
    return render(request, 'music/create_playlist.html')

@login_required
def add_to_playlist(request, song_id, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    song = get_object_or_404(Song, id=song_id)
    playlist.songs.add(song)
    messages.success(request, f'"{song.title}" added to {playlist.name}')
    return redirect('music:playlist_detail', pk=playlist.pk)

@login_required
def remove_from_playlist(request, playlist_id, song_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        song = get_object_or_404(Song, id=song_id)
        playlist.songs.remove(song)
        messages.success(request, f'"{song.title}" removed from {playlist.name}')
    return redirect('music:playlist_detail', pk=playlist_id)


# views.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import requests

@login_required
@require_POST

def play_track(request):
    data = json.loads(request.body)
    uri = data.get('uri')
    device_id = data.get('device_id')
    
    # Get the user's Spotify access token from your authentication system
    access_token = request.user.spotify_token  # Adjust based on your auth implementation
    
    # Call Spotify API to start playback
    response = requests.put(
        f'https://api.spotify.com/v1/me/player/play?device_id={device_id}',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        },
        json={
            'uris': [uri]
        }
    )
    
    if response.status_code in [200, 204]:
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# Update your AlbumDetailView
class AlbumDetailView(DetailView):
    model = Album
    template_name = 'music/album_detail.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = self.object.songs.all()

        # Add Spotify token to context only if not running locally
        if not settings.DEBUG and self.request.user.is_authenticated:
            context['spotify_token'] = self.request.user.spotify_token  # Adjust based on your auth implementation
        
        return context
