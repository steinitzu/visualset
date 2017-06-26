from functools import partial
from itertools import cycle
import math

from giveme import inject, register
from speedyspotify import Spotify

from .entities import Line
from .util import chunked, sampled_songs, most_prominent, uniquify


@inject
def recommendations(spotify_client: Spotify, artists, line: Line):
    """
    Yield recommendations chunks that can be used to construct a playlist on a line.
    """
    artists = cycle(chunked(artists, 5))
    me = spotify_client.me().fetch()
    min_attr = 'min_'+line.attribute_name
    max_attr = 'max_'+line.attribute_name

    for r in line.ranges:
        if r.left == r.right or abs(r.left-r.right) < 0.1:
            # Set so we get some songs
            r.left = max(r.left-0.03, 0.0)
            r.right = min(r.right+0.03, 1.0)
        params = {
            min_attr: min(r.left, r.right),
            max_attr: max(r.left, r.right),
            'min_valence': min(r.left, r.right),
            'max_valence': max(r.left, r.right)
        }
        print(r)
        tracks = spotify_client.recommendations(
            seed_artists=next(artists),
            country=me['country'],
            limit=100,
            **params
        ).fetch()['tracks']
        tracks += spotify_client.recommendations(
            seed_artists=next(artists),
            country=me['country'],
            limit=100,
            **params
        ).fetch()['tracks']

        tracks = list(uniquify(tracks, 'id'))

        audio_features = spotify_client.audio_features.all(tracks).fetch('items')
        for i, af in enumerate(audio_features):
            tracks[i]['audio_features'] = af

        tracks = sorted(
            tracks,
            key=lambda x: x['audio_features'][line.attribute_name], reverse=r.reverse
        )
        ntracks = math.ceil(r.duration_seconds/(60*3))  # let's say average song length is 3 minutes for now
        sampled = sampled_songs(tracks, line.attribute_name, r.left, r.right, ntracks)
        yield sampled


@inject
def save_playlist(spotify_client: Spotify, name, songs):
    me = spotify_client.me().fetch()
    playlist = spotify_client.user_playlist_create(me, name).fetch()
    spotify_client.user_playlist_add_tracks.all(songs, me, playlist).fetch()
    return playlist


@inject
def saved_songs(spotify_client: Spotify):
    yield from spotify_client.ijoin(
        spotify_client.current_user_saved_tracks.all()
    )


@inject
def saved_albums(spotify_client: Spotify):
    yield from spotify_client.ijoin(
        spotify_client.current_user_saved_albums.all()
    )


@inject
def followed_artists(spotify_client: Spotify):
    result = spotify_client.current_user_followed_artists(limit=50)
    while result:
        result = result.fetch()['artists']
        yield from result['items']
        result = spotify_client.next(result)


@inject
def top_artists(spotify_client: Spotify, term='short_term'):
    yield from spotify_client.ijoin(
        spotify_client.current_user_top_artists.all(time_range=term)
    )


def library_artists(saved_songs, saved_albums, followed_artists, top_artists):
    """
    Yield artists from followed artists, all saved songs and
    saved_albums
/    """
    for song in saved_songs:
        yield from song['track']['artists']

    for album in saved_albums:
        yield from album['album']['artists']

    yield from followed_artists
    yield from top_artists


@inject
def most_prominent_artists(count=20):
    yield from most_prominent(
        library_artists(
            saved_songs(),
            saved_albums(),
            followed_artists(),
            top_artists(term='short_term')
        ),
        count=count, key='id'
    )

    # yield from most_prominent(library_artists, count=count, key='id')
