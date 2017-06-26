from flask import session

from giveme import inject, register
from speedyspotify.oauth2 import SpotifyOAuth
from speedyspotify import Spotify

from . import config


@register
def spotify_client_config():
    return {
        'client_id': config.SPOTIFY_CLIENT_ID,
        'client_secret': config.SPOTIFY_CLIENT_SECRET,
        'redirect_uri': config.SPOTIFY_REDIRECT_URI,
        'scope': config.SPOTIFY_SCOPE
    }


@register
def spotify_token():
    return session['spotify_token']


@register
@inject
def spotify_auth(spotify_client_config):
    return SpotifyOAuth(**spotify_client_config)


@register(threadlocal=True)
@inject
def spotify_client(spotify_token, spotify_client_config):

    class S(Spotify):
        _client_id = spotify_client_config['client_id']
        
        def _auth_headers(self):
            headers = super()._auth_headers()
            headers['Spotify-Client-Id'] = self._client_id
            headers['refreshtoken'] = spotify_token['refresh_token']
            return headers
    
    s = S(access_token=spotify_token, gpool=True, gpool_size=5, pool_size=20)
    s.prefix = config.SPOTPROXY_URL+'/v1'
    return s
