from giveme import inject, register
from speedyspotify.oauth2 import SpotifyOAuth
from speedyspotify import Spotify


@register
def spotify_client_config():
    return {
        'client_id': '31c19656d19b45539ed22ad58aa0459c',
        'client_secret': '0512031d8ecb4611893988f2d428097d',
        'redirect_uri': 'http://localhost/spotify/auth/callback'
    }


@register
@inject
def spotify_token(spotify_auth):
    refresh_token = 'AQBDmSBjpVQwR5kajjSe8S2pGuafzZyuzKtykYoxxfKKTYCJ2z1ajV0XarO56ENoC3niEjyJ4y3mx1AB2WeqU8lLo1dvO6Cyk9BH6Hc6cDt6MAB-uV8ngRjRwjyShU8qah4'  # NOQA
    new_token = spotify_auth.refresh_access_token(refresh_token)
    return new_token


@register
@inject
def spotify_auth(spotify_client_config):
    return SpotifyOAuth(**spotify_client_config)


@register
@inject
def spotify_client(spotify_token, spotify_client_config):

    class S(Spotify):
        def _auth_headers(self):
            headers = super()._auth_headers()
            headers['refreshtoken'] = spotify_token['refresh_token']
            return headers
    
    s = S(access_token=spotify_token, gpool=True, gpool_size=5, pool_size=20)
    s.prefix = 'http://localhost:8080/v1'
    return s
