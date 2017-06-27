from time import time

from giveme import inject


@inject
def authorize_url(spotify_auth):
    return spotify_auth.get_authorize_url()


@inject
def access_token(spotify_auth, url):
    """
    Get access token from callback response code
    """
    code = spotify_auth.parse_response_code(url)
    return spotify_auth.get_access_token(code)


def expires_in(timestamp):
    return time.time() - timestamp


@inject
def refresh_if_needed(spotify_auth, token_info, expired_minutes=10):
    if expires_in(token_info['expires_in']) > expired_minutes*60:
        return token_info
    token = spotify_auth.refresh_token(token_info['refresh_token'])
    if not token:
        raise ValueError('Invalid or revoked refresh token')
    return token
