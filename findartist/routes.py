import time

import spotipy
import spotipy.util as util
from flask import Blueprint, render_template, redirect, url_for, current_app, session, request, abort, flash
from rq.exceptions import NoSuchJobError
from rq.job import Job

from findartist.forms import ArtistForm
from findartist.spotify import generate_playlist

main = Blueprint("main", __name__, static_folder='static')


@main.route('/findartist', methods=['GET'])
def findartist():
    """
    The main page of the application.
    :return: renders the page.
    """
    form = ArtistForm()
    return render_template('findartist.html', form=form)


@main.route('/')
def verify():
    """
    Spotify authorization code flow step 1. See
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
    :return: redirects user to Spotify's authorization page
    """
    # https://stackoverflow.com/a/57929497/6538328
    scope = 'playlist-modify-private,playlist-modify-public,user-top-read'
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=current_app.config['SPOTIFY_CLIENT_ID'],
                                           client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
                                           redirect_uri=current_app.config['REDIRECT_URL'],
                                           scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@main.route('/callback')
def callback():
    """
    Spotify authorization code flow step 2. See
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
    :return: redirects user to the application
    """
    # https://stackoverflow.com/a/57929497/6538328
    scope = 'playlist-modify-private,playlist-modify-public,user-top-read'
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=current_app.config['SPOTIFY_CLIENT_ID'],
                                           client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
                                           redirect_uri=current_app.config['REDIRECT_URL'],
                                           scope=scope,
                                           username="FindSimilarArtists")
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info

    return redirect(url_for("main.findartist"))


@main.route('/findartist', methods=['POST'])
def post_artist():
    """
    Spotify authorization code flow step 3. See
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow

    Processes form input and, if valid, calls generate_playlist().

    :return: redirects to itself and displays a message depending on success.
    """
    # Session validation
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        return redirect(url_for('main.verify'))

    # Initialize variables
    form = ArtistForm()

    client_credentials_manager = spotipy.SpotifyClientCredentials(client_id=current_app.config['SPOTIFY_CLIENT_ID'],
                                                                  client_secret=current_app.config[
                                                                      'SPOTIFY_CLIENT_SECRET'])
    sp_app = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp_user = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    # If user input is valid, proceed. Else, try again.
    if form.validate_on_submit():
        job = current_app.task_queue.enqueue_call(func=generate_playlist,
                                                  args=(form.artist.data, sp_user, sp_app),
                                                  result_ttl=3600)
        job_id = job.get_id()
        print(job_id)
        flash(f"Playlist creation in process. Go to {url_for('main.get_results', job_key=job_id)}")
        return redirect(url_for('main.findartist'))
    else:
        print('form didnt validate')
        return redirect(url_for('main.findartist'))


def get_token(curr_session: session):
    """
    Checks to see if token is valid and gets a new token if not
    :param curr_session: A flask session object
    :return: a tuple that contains token info and a boolean representing the validity of the token
    """
    token_valid = False
    token_info = curr_session.get("token_info", {})
    scope = 'playlist-modify-private,playlist-modify-public,user-top-read'
    # Checking if the session already has a token stored
    if not (curr_session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = curr_session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if is_token_expired:
        # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse
        # a SpotifyOAuth object
        sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=current_app.config['SPOTIFY_CLIENT_ID'],
                                               client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=current_app.config['REDIRECT_URL'],
                                               scope=scope)
        token_info = sp_oauth.refresh_access_token(curr_session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


@main.route('/results/<job_key>')
def get_results(job_key):
    try:
        job = Job.fetch(job_key, connection=current_app.redis)
    except NoSuchJobError:
        return "Job not found."
    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202
