import os

SPOTIFY_CLIENT_ID = os.environ['VISUALSET_SPOTIFY_ID']
SPOTIFY_CLIENT_SECRET = os.environ['VISUALSET_SPOTIFY_SECRET']
SPOTIFY_REDIRECT_URI = os.environ['VISUALSET_SPOTIFY_CALLBACK']

SPOTIFY_SCOPE = ' '.join([
    'user-follow-read',
    'user-library-read',
    'user-top-read',
    'playlist-modify-public',
    'user-read-private',
])

SPOTPROXY_URL = os.environ['SPOTPROXY_URL']


