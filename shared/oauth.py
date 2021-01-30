from spotipy import oauth2
from .config import base_url

SPOTIPY_CLIENT_ID = "9dacc40b7cf6403289c13726ae7a6647"
SPOTIPY_CLIENT_SECRET = "27e24d7036974055813ea973024b3a0c"
SPOTIPY_REDIRECT_URI = base_url + "auth_callback"
SCOPE = 'user-library-read playlist-read-private ugc-image-upload user-read-playback-state user-read-email playlist-read-collaborative user-modify-playback-state user-read-private playlist-modify-public user-library-modify user-top-read user-read-playback-position user-read-currently-playing user-follow-read user-read-recently-played user-follow-modify'

sp_oauth = oauth2.SpotifyOAuth(
	SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,
	SPOTIPY_REDIRECT_URI, scope=SCOPE
)