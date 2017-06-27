from functools import wraps

from flask import (
    Flask,
    redirect,
    request,
    session,
    url_for,
    jsonify,
    send_from_directory,
    make_response
)

from visualset.api import produce_playlist
from visualset.spotify_auth import authorize_url, access_token, refresh_if_needed


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdj90ajsd90jas9dija0sd'


def spotify_login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        current_token = session['spotify_token']
        try:
            new_token = refresh_if_needed(current_token, expired_minutes=10)
        except ValueError as e:
            return make_response(jsonify(dict(error=str(e))), 403)
        else:
            session['spotify_token'] = new_token
        return func(*args, **kwargs)
    return decorator


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
@spotify_login_required
def submit_line():
    data = request.get_json()
    playlist = produce_playlist(data, audio_attribute='energy')
    return jsonify(playlist)
