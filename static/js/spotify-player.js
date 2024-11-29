let player;
let deviceId;
let currentTrack = null;
let isPlaying = false;

window.onSpotifyWebPlaybackSDKReady = () => {
    // Only load token and initialize player in production mode
    const isLocal = document.getElementById('is-local')?.content === 'true'; // Flag for local environment
    const token = !isLocal ? document.getElementById('spotify-token')?.content : null;

    if (!token && !isLocal) {
        console.warn('No Spotify token found');
        return;
    }

    if (isLocal) {
        console.log('Running locally, skipping Spotify token initialization.');
        return;
    }

    player = new Spotify.Player({
        name: 'Spotify Clone Web Player',
        getOAuthToken: cb => { cb(token); },
        volume: 0.5
    });

    // Error handling
    player.addListener('initialization_error', ({ message }) => {
        console.error('Failed to initialize:', message);
    });
    player.addListener('authentication_error', ({ message }) => {
        console.error('Failed to authenticate:', message);
    });
    player.addListener('account_error', ({ message }) => {
        console.error('Failed to validate Spotify account:', message);
    });
    player.addListener('playback_error', ({ message }) => {
        console.error('Failed to perform playback:', message);
    });

    // Playback status updates
    player.addListener('player_state_changed', state => {
        if (!state) return;

        currentTrack = state.track_window.current_track;
        isPlaying = !state.paused;

        // Update play/pause button
        const playIcon = document.getElementById('play-icon');
        playIcon.classList.remove('fa-play-circle', 'fa-pause-circle');
        playIcon.classList.add(isPlaying ? 'fa-pause-circle' : 'fa-play-circle');

        // Update track information
        document.getElementById('current-track-name').textContent = currentTrack.name;
        document.getElementById('current-track-artist').textContent = currentTrack.artists.map(artist => artist.name).join(', ');

        if (currentTrack.album.images.length > 0) {
            document.getElementById('current-track-image').src = currentTrack.album.images[0].url;
        }

        // Update progress bar
        updateProgress(state.position, state.duration);
    });

    // Ready
    player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
        deviceId = device_id;

        // Store device ID for use in play requests
        localStorage.setItem('spotify_device_id', device_id);
    });

    // Not Ready
    player.addListener('not_ready', ({ device_id }) => {
        console.log('Device ID has gone offline', device_id);
    });

    // Connect to the player
    player.connect();

    // Setup controls
    setupControls();
};

function setupControls() {
    // Play/Pause
    document.getElementById('toggle-play').addEventListener('click', () => {
        if (!player) return;
        player.togglePlay();
    });

    // Previous track
    document.getElementById('previous-track').addEventListener('click', () => {
        if (!player) return;
        player.previousTrack();
    });

    // Next track
    document.getElementById('next-track').addEventListener('click', () => {
        if (!player) return;
        player.nextTrack();
    });

    // Volume control
    document.getElementById('volume-control').addEventListener('input', (e) => {
        if (!player) return;
        const volume = parseInt(e.target.value) / 100;
        player.setVolume(volume);
    });
}

// Function to update progress bar
function updateProgress(position, duration) {
    const progressBar = document.getElementById('playback-progress');
    const progress = (position / duration) * 100;
    progressBar.style.width = `${progress}%`;

    // Update time displays
    document.getElementById('current-time').textContent = formatTime(position);
    document.getElementById('duration').textContent = formatTime(duration);
}

// Format milliseconds to mm:ss
function formatTime(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Function to play a specific track
async function playTrack(uri) {
    if (!deviceId) {
        console.error('No device ID available');
        return;
    }

    try {
        await fetch('/play-track/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                uri: uri,
                device_id: deviceId
            })
        });
    } catch (error) {
        console.error('Error playing track:', error);
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
