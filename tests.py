import logging
import sys
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
requests_log.addHandler(logging.StreamHandler(stream=sys.stdout))

from itertools import chain
from random import shuffle

from visualset import dependencies
from visualset import songrepo
from visualset import entities

# bad manual tests

# artists = {
#     'The new pornographers': '4mO4aGO6u29UyR6XLZR9XW',
#     'Fatboy Slim': '4Y7tXHSEejGu1vQ9bwDdXW',
#     'Sigur ros': '6UUrUCIZtQeOf8tC0WuzRy',
#     'Eels': '3zunDAtRDg7kflREzWAhxl'
# }

# songs = songrepo.get_recommendations(
#     seed_artists=list(artists.values()),
#     low_mood=2,
#     high_mood=9,
#     duration_seconds=60*60
# )

# playlist = songrepo.save_playlist('visualset', songs)


# for track in songrepo.get_saved_songs():
#     print(track['track']['id'])

# for artist in songrepo.artist_list():
#     print(artist['id'])


most_prominent = list(songrepo.most_prominent_artists(40))
print('\n'.join([i['id'] for i in most_prominent]))
shuffle(most_prominent)

AR = entities.AttributeRange
# ranges = [
#     AR(0.1, 0.9, 12*60),
#     AR(0.9, 0.5, 12*60),
#     AR(0.5, 0.2, 12*60),
#     AR(0.2, 0.7, 12*60),
#     AR(0.7, 0.3, 12*60)
# ]

ranges = [
    AR(0.0, 1.0, 12*60),
    AR(1.0, 0.0, 12*60)
]
line = entities.Line(
    'energy',
    *ranges
)

line = entities.Line(
    'valence',
    *ranges
)

songs = songrepo.recommendations(most_prominent, line)

songrepo.save_playlist('VisualSet', chain(*songs))


# for i in most_prominent:
#     print(i['id'], i['name'])



# print([i['id'] for i in songrepo.get_saved_songs()])
