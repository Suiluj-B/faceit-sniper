import requests
from flask import Flask, request, session, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Geheime Schlüssel für die Sitzungsverwaltung
api_key = "bbc65b04-9802-42d1-889d-9b52f1b42166"

@app.route('/webhook', methods=['POST'])
def webhook():
    match = request.json

    # Überprüfen, ob das Match bereits in der Sitzung enthalten ist
    if match['match_id'] not in session.get('matches', []):
        session.setdefault('matches', []).append(match['match_id'])

    # Vergleichen der JSON-Payloads, um geeignete Ausgabe zu generieren
    if session.get('matches'[0]) == session.get('matches'[1]):
        print('Match sniped!')
    else:
        print('Match nicht sniped!')

    # Code für die Ausgabe hier
    user_id = session.get('user_id', None)
    matches = session.get('matches', [])
    return render_template('index.html', user_id=user_id, matches=matches)


@app.route('/', methods=['GET', 'POST'])
def index():
    user_id = session.get('user_id', None)
    matches = session.get('matches', [])

    if request.method == 'POST':
        username = request.form['username']
        response = requests.get(f'https://open.faceit.com/data/v4/players?nickname={username}',
                                headers={'Authorization': 'Bearer ' + api_key})
        if response.ok:
            user_id = response.json()['player_id']
            session['user_id'] = user_id
        else:
            error = 'Spieler nicht gefunden'
            return render_template('index.html', error=error)

    return render_template('index.html', user_id=user_id, matches=matches)


if __name__ == '__main__':
    app.run(debug=True)
