# music/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)
    spotify_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    spotify_url = models.URLField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cover = models.ImageField(upload_to='albums/', blank=True, null=True)
    release_date = models.DateField(default=timezone.now)
    genre = models.CharField(max_length=100)
    spotify_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    spotify_uri = models.CharField(max_length=255, blank=True, null=True)
    total_tracks = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    class Meta:
        ordering = ['-release_date']

class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    duration_ms = models.IntegerField(default=0)  # Duration in milliseconds (Spotify format)
    track_number = models.PositiveIntegerField()
    spotify_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    spotify_uri = models.CharField(max_length=255, blank=True, null=True)
    preview_url = models.URLField(max_length=255, blank=True, null=True)
    is_playable = models.BooleanField(default=True)
    popularity = models.IntegerField(default=0)  # Spotify popularity index (0-100)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['album', 'track_number']
        unique_together = ['album', 'track_number']

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='playlist_covers/', blank=True, null=True)
    spotify_id = models.CharField(max_length=255, blank=True, null=True)
    spotify_uri = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']

# Optional: Create a model to store user's Spotify credentials
class SpotifyToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_type = models.CharField(max_length=50)
    expires_in = models.DateTimeField()
    
    def is_expired(self):
        return timezone.now() >= self.expires_in