#!/usr/bin/env python
import re
from datetime import datetime, timedelta

import flask
from flask import abort, jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
silences = [
    {
        'silence': "qu*x",
        'expiry': datetime.now() + timedelta(minutes=10)
    },
    {
        'silence': "bar.*",
        'expiry': datetime.now() + timedelta(minutes=10)
    },
    {
        'silence': "foo.*",
        'expiry': datetime.now() + timedelta(minutes=10)
    }
]


def cleanup_expired_silences():
    '''modify the global silences dictionary to remove any silences that have expired'''
    global silences
    # silences = list(filter(lambda silence: silence.get('expiry') > datetime.now(), silences))
    silences = [s for s in silences if s.get('expiry') > datetime.now()]


@app.route('/', methods=['GET'])
def home():
    '''home page contains the current silence regex list and their expiry times'''
    page_content = '''<h1>This is your magical home for create silences</h1>
    <p>Create a silence here for your alerts</p><ul>'''

    for silence in silences:
        page_content += f"<li>{silence.get('silence')} - {silence.get('expiry')}</li>"

    page_content += '</ul>'

    return page_content


@app.route('/api/v1/resources/alerts', methods=['POST'])
def api_alert():
    '''the api enpoint hit to determine if an alert should be filtered or not based on the current list of silences'''
    if not request.json or 'alert' not in request.json:
        abort(400)

    cleanup_expired_silences()
    combined = "(" + ")|(".join(silences) + ")"

    if re.match(combined, request.json.get('alert', "")):
        return jsonify({'silenced': True})
    else:
        return jsonify({'silenced': False})


@app.route('/api/v1/resources/silence', methods=['POST'])
def api_silence():
    '''api endpoint used to set a new silence'''
    if not request.json or 'silence' not in request.json or 'expiry' not in request.json:
        abort(400)
    silence = {
        'silence': request.json.get('silence', ""),
        'expiry': datetime.now() + timedelta(minutes=int(request.json.get('expiry', 0)))
    }
    silences.append(silence)
    return jsonify({'silence': silence}), 201


@app.route('/api/v1/resources/alerts/all', methods=['GET'])
def api_silence_all():
    '''api endpoint used to list current silences'''
    return jsonify(silences)


app.run(host="0.0.0.0")
