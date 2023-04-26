from flask import Flask, request, jsonify, session
import json  # JSON-Modul importieren
import datetime

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()  # JSON-Payload aus der Anfrage abrufen
    print(data, data['entity'])  # JSON-Payload ausgeben
    entity_id = data['entity']['id']  # Entity-ID aus der JSON-Payload abrufen
    now = datetime.datetime.now()
    print(now)
    save_json({'match_id': entity_id, 'received at:': '{}'.format(now)},
              '{}.json'.format(data['player_id']))  # JSON-Payload in eine Datei speichern
    print('Match ID: {}'.format(entity_id))
    return jsonify({'message': 'Webhook received successfully'}), 200  # Erfolgreiche Anfrage zurückgeben


def save_json(payload, filename):
    with open(filename, 'w') as f:
        json.dump(payload, f)


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    app.run(port=5000)
