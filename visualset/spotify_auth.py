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
