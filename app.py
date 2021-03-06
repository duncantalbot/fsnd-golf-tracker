from os import environ as env
import os
from werkzeug.exceptions import HTTPException
from functools import wraps

from flask import (
    Flask,
    request,
    jsonify,
    abort,
    redirect,
    render_template,
    session,
    url_for)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from models import setup_db, Person, Event
import json

from auth import AuthError, requires_auth, requires_signed_in
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode


AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_BASE_URL = 'https://' + os.environ['AUTH0_DOMAIN']
AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']

app = Flask(__name__)
setup_db(app)

CORS(app)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


'''
AUTHENTICATION
'''


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/login-results')
def callback_handling():
    # Handles response from token endpoint
    res = auth0.authorize_access_token()
    token = res.get('access_token')

    # Store the user information in flask session.
    session['jwt_token'] = token

    return redirect('/dashboard')


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    print('logout')
    # Redirect user to logout endpoint
    params = {'returnTo': url_for(
        'home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/dashboard')
@requires_signed_in
def dashboard():
    return render_template('dashboard.html', token=session['jwt_token'],)


'''
PERSONS
'''


@app.route("/persons", methods=['GET'])
@requires_auth('get:events')
def get_persons(jwt):

    try:
        persons = Person.query.all()

        return jsonify({
            'success': True,
            'persons': [person.serialize() for person in persons]
        })
    except exception:
        abort(404)


@app.route("/persons", methods=['POST'])
@requires_auth('post:events')
def add_person(jwt):

    body = request.get_json()

    if not ('firstname' in body and 'lastname' in body and 'handicap' in body):
        abort(404)

    firstname = body.get('firstname')
    lastname = body.get('lastname')
    handicap = body.get('handicap')

    try:
        person = Person(
            firstname=firstname, lastname=lastname, handicap=handicap)
        person.insert()

        return jsonify({
            'success': True
        })

    except Exception:
        abort(422)


@app.route("/persons/<id>", methods=['PATCH'])
@requires_auth('update:events')
def update_person(jwt, id):

    person = Person.query.get(id)

    if person:
        try:
            body = request.get_json()

            firstname = body.get('firstname')
            lastname = body.get('lastname')
            handicap = body.get('handicap')

            if firstname:
                person.firstname = firstname
            if lastname:
                person.lastname = lastname
            if handicap:
                person.handicap = handicap

            person.update()

            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)
    else:
        abort(404)


@app.route("/persons/<id>", methods=['DELETE'])
@requires_auth('delete:events')
def delete_person(jwt, id):

    person = Person.query.get(id)

    if person:
        try:
            person.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except Exception:
            abort(422)
    else:
        abort(404)


'''
EVENTS
'''


@app.route("/events", methods=['GET'])
@requires_auth('get:events')
def get_events(jwt):

    try:
        events = Event.query.all()

        return jsonify({
            'success': True,
            'events': [event.serialize() for event in events]
        })
    except Exception:
        abort(404)


@app.route("/events", methods=['POST'])
@requires_auth('post:events')
def add_event(jwt):

    body = request.get_json()

    if not ('event_type' in body and 'date' in body and 'description' in body):
        abort(404)

    event_type = body.get('event_type')
    date = body.get('date')
    description = body.get('description')

    try:
        event = Event(
            event_type=event_type,
            date=date,
            description=description)
        event.insert()

        return jsonify({
            'success': True
        })

    except Exception:
        abort(422)


'''
Error Handling
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": str(error)
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": str(error)
    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
        "success": False,
        "error": ex.status_code,
        'message': ex.error
    }), 401


if __name__ == '__main__':
    app.run()
