# music/admin.py
from django.contrib import admin
from .models import Artist, Album, Song, Playlist, SpotifyToken

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'spotify_id', 'bio')
    search_fields = ('name', 'spotify_id')
    list_filter = ('name',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'genre', 'spotify_id', 'total_tracks')
    list_filter = ('genre', 'release_date')
    search_fields = ('title', 'artist__name', 'spotify_id')
    autocomplete_fields = ['artist']
    date_hierarchy = 'release_date'

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'track_number', 'duration', 'spotify_id', 'is_playable', 'popularity')
    list_filter = ('album', 'artist', 'is_playable')
    search_fields = ('title', 'album__title', 'artist__name', 'spotify_id')
    autocomplete_fields = ['album', 'artist']
    ordering = ('album', 'track_number')
    readonly_fields = ('spotify_uri', 'spotify_id', 'preview_url', 'popularity')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'is_public', 'spotify_id')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'user__username', 'spotify_id')
    filter_horizontal = ('songs',)
    date_hierarchy = 'created_at'

@admin.register(SpotifyToken)
class SpotifyTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_type', 'expires_in', 'is_expired')
    readonly_fields = ('access_token', 'refresh_token', 'token_type', 'expires_in')
    search_fields = ('user__username',)
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'

# Customize admin site header and title
admin.site.site_header = 'Spotify Clone Admin'
admin.site.site_title = 'Spotify Clone Admin Portal'
admin.site.index_title = 'Welcome to Spotify Clone Admin Portal'