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

from visualset.api import produce_playlist
from visualset.spotify_auth import authorize_url, access_token


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
    playlist = produce_playlist(data, audio_attribute='energy')
    return jsonify(playlist)
