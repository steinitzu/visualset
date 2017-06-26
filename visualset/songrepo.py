from functools import partial
from collections import Counter
from itertools import cycle
from random import sample
import math

from giveme import inject, register
from speedyspotify import Spotify

from .entities import AttributeRange, Line
from .util import chunked, sampled_songs


@inject
def get_recommendations(spotify_client: Spotify,
                        seed_artists: list,
                        low_mood: int,
                        high_mood: int,
                        duration_seconds: int,
                        order='asc'):
    s = spotify_client
    me = s.me().fetch()

    low_energy = low_mood/10
    mid_energy = ((high_mood+low_mood)/2)/10
    high_energy = high_mood/10

    recommendations = partial(
        s.recommendations,
        seed_artists=seed_artists, limit=10,
        country=me['country']
    )

    low_songs = recommendations(max_energy=low_energy)
    mid_songs = recommendations(min_energy=low_energy, max_energy=high_energy,
                                target_energy=mid_energy)
    high_songs = recommendations(min_energy=high_energy)

    songs = s.join([low_songs, mid_songs, high_songs], extract=True)
    audio_features = s.audio_features.all(songs).fetch('items')

    for i, af in enumerate(audio_features):
        songs[i]['audio_features'] = af

    return sorted(songs, key=lambda x: x['audio_features']['energy'])


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
        if r.left == r.right:
            # Set so we get some songs
            r.left = max(r.left-0.05, 0.0)
            r.right = min(r.right+0.05, 1.0)
        params = {
            min_attr: min(r.left, r.right),
            max_attr: max(r.left, r.right),
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

        audio_features = spotify_client.audio_features.all(tracks).fetch('items')
        for i, af in enumerate(audio_features):
            tracks[i]['audio_features'] = af

        tracks = sorted(tracks, key=lambda x: x['audio_features'][line.attribute_name], reverse=r.reverse)
        ntracks = math.ceil(r.duration_seconds/(60*3))  # let's say average song length is 3 minutes for now
        sampled = sampled_songs(tracks, line.attribute_name, r.left, r.right, ntracks)
        yield sampled


@inject
def save_playlist(spotify_client: Spotify, name, songs):
    me = spotify_client.me().fetch()
    playlist = spotify_client.user_playlist_create(me, name).fetch()
    spotify_client.user_playlist_add_tracks.all(songs, me, playlist).fetch()
    return playlist


@register
@inject
def saved_songs(spotify_client: Spotify):
    yield from spotify_client.ijoin(
        spotify_client.current_user_saved_tracks.all()
    )


@register
@inject
def saved_albums(spotify_client: Spotify):
    yield from spotify_client.ijoin(
        spotify_client.current_user_saved_albums.all()
    )


@register
@inject
def followed_artists(spotify_client: Spotify):
    result = spotify_client.current_user_followed_artists(limit=50)
    while result:
        result = result.fetch()['artists']
        yield from result['items']
        result = spotify_client.next(result)


@register
@inject
def top_artists(spotify_client: Spotify, term='short_term'):
    yield from spotify_client.ijoin(
        spotify_client.current_user_top_artists.all(time_range=term)
    )


@register    
@inject
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
def most_prominent_artists(library_artists, count=20):
    yield from most_prominent(library_artists, count=count, key='id')


def uniquify(items, key='id'):
    """
    From a sequence of dicts, yield each unique item only once.
    Uniqueness of an item is determined by the provided key.

    Args:
        items (sequence): A sequence of dictionaries containing `key`
        key (hashable type): The dictionary key that determines uniqueness
    Returns:
        generator
    """
    seen = set()
    seen_add = seen.add
    for item in items:
        if item[key] in seen:
            continue
        seen_add(item[key])
        yield item


def most_prominent(items, count=20, key='id'):
    """
    From a sequence of dicts yield the `count` most
    prominent items by value of `key`
    """
    items = sorted(items, key=lambda x: x[key])
    item_keys = (item[key] for item in items)
    items_by_key = {item[key]: item for item in items}
    
    counter = Counter(item_keys)

    return (items_by_key[k] for k, v in counter.most_common(count))

