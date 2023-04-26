#from flask import Flask, request, jsonify, render_template
from flask import *
import requests
import json
import makerequest
import time


app = Flask(__name__, template_folder='templates')

def save_json(payload, filename):
    with open(filename, 'w') as f:
        json.dump(payload, f)


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)



@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def process_form():
    print("LOL")
    url = "https://open.faceit.com/data/v4/players?nickname="
    username = request.form.get("username")
    redirected_url = "home"
    app.result = {"player_id": makerequest.getPlayerIDfromUsername(username), "username": username}

    return redirect(url_for(redirected_url, result=app.result))


'''def rerender_index(*vars):
    return render_template("index.html", result = "test")'''

@app.route('/sniping', methods=['POST', 'GET'])
def rerender_sniping():
    if request.method == 'POST':
        # do some processing here
        result = "some result"
        return render_template("sniping.html", result=result)
    else:
        return render_template('sniping.html')# Find a way to rerender the page with optional parameters.


def snipe():
    app.sniping_status = "Sniping..."
    print("sniping")
    sniper_id = request.form.get("sniper_id")
    target_id = request.form.get("target_id")
    print("reached")

    return sniping(sniper_id, target_id)

def sniping(sniper_id, target_id):
    sniper_payload = load_json('{}.json'.format(sniper_id))
    target_payload = load_json('{}.json'.format(target_id))
    old_sniper_payload = sniper_payload
    app.sniping_status = 'Sniper started...'
    while True:
        new_sniper_payload = load_json('{}.json'.format(sniper_id))
        print(new_sniper_payload)
        time.sleep(1)
        if new_sniper_payload['entity']['id'] != old_sniper_payload['entity']['id']:
            print('Sniper payload changed!')
            sniping_status = 'Found one match...'
            while True:
                time.sleep(5)
                new_target_payload = load_json('{}.json'.format(target_id))
                print("reached here")
                if new_target_payload != target_payload:
                    if new_sniper_payload['entity']['id'] == new_target_payload['entity']['id']:
                        sniping_status = 'Sniped!'
                        print('Sniped!')
                        return
                else:
                    sniping_status = 'Waitin for target update...'
                    print('Waiting for target update...')

    return





def receiveMatchID():
    data = request.get_json()  # JSON-Payload aus der Anfrage abrufen
    print(data['transaction_id'], data['entity'])  # JSON-Payload ausgeben
    entity_id = data['entity']['id']  # Entity-ID aus der JSON-Payload abrufen
    app.id_comparison(entity_id, app.getPlayerID())  # Vergleich der Entity-ID mit der Player-ID
    return entity_id


@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-Faceit-Event')
    # if event_type == 'match_object_created':
    payload = request.get_json()
    if 'entity' in payload:
        app.match_id = payload['entity']['id']
        save_json(payload, '{}.json'.format(payload['player_id']))
        print('Match ID: {}'.format(app.match_id))
        return 'Match ID: {}'.format(app.match_id)
    else:
        return 'No match ID found', 404





def createSniperID():
    sniperID = request.form.get("sniper_id")
    return sniperID

@app.route('/compare', methods=['POST'])
def compare():
    payloadNow = request.get_json()
    try:
        sniperPayload = load_json('{}.json'.format(app.sniperID))
    except FileNotFoundError:
        return 'No previous match found', 404
    finally:
        if payloadNow['entity']['id'] == oldPayload['entity']['id']:
            return 'Match IDs are the same'
        else:
            return 'Match IDs are different'


if __name__ == '__main__':
    app.run(debug=True)
