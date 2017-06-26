from itertools import chain
from random import shuffle

from . songrepo import (
    recommendations,
    save_playlist,
    most_prominent_artists
)
from . entities import (
    Line,
    AttributeRange as AR
)


def produce_playlist(data, audio_attribute='energy'):
    ranges = []
    last_point = None
    for i, point in enumerate(data['points']):
        if i == 0:
            last_point = point
            continue
        energy = point['energy']/100
        minute = point['minute']
        last_energy = last_point['energy']/100
        last_minute = last_point['minute']

        duration = (minute-last_minute)*60

        ranges.append(AR(last_energy, energy, duration))
        last_point = point
    line = Line(audio_attribute, *ranges)

    artists = list(most_prominent_artists(count=15))
    shuffle(artists)
    songs = recommendations(artists, line)
    playlist = save_playlist('VisualSet', chain(*songs))
    return playlist
                   
