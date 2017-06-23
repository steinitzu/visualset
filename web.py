from itertools import chain
from random import shuffle

from flask import (
    Flask,
    redirect,
    request,
    session,
    url_for,
    jsonify,
    send_from_directory
)

from visualset.spotify_auth import authorize_url, access_token
from visualset.entities import AttributeRange, Line
from visualset.songrepo import recommendations, save_playlist, most_prominent_artists


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdj90ajsd90jas9dija0sd'


@app.route('/')
def index():
    return send_from_directory('web', 'index.html')


@app.route('/js/<path:path>')
def js(path):
    return send_from_directory('web', path)


@app.route('/spotify/authorize')
def authorize():
    return redirect(authorize_url())


@app.route('/spotify/callback')
def callback():
    token = access_token(request.url)
    session['spotify_token'] = token
    return redirect(url_for('index'))


@app.route('/api/lines', methods=['POST'])
def submit_line():
    data = request.get_json()
    AR = AttributeRange
    print(data)
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

    line = Line('energy', *ranges)
    print(line)

    artists = list(most_prominent_artists(count=15))
    shuffle(artists)
    songs = recommendations(artists, line)
    playlist = save_playlist('VisualSet', chain(*songs))
    return jsonify(playlist)
