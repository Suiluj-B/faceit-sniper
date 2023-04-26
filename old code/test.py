import requests
from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'secret_key'
app.api_key = 'bbc65b04-9802-42d1-889d-9b52f1b42166'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_name_1 = request.form['player_name_1']
        player_name_2 = request.form['player_name_2']
        print(player_name_1)
        print(player_name_2)
        session['player_name_1'] = player_name_1
        session['player_name_2'] = player_name_2
        return render_template('index.html')

    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if request.method != 'POST':
        return render_template('index.html')
    print(session.get('player_name_1'))
    print(session.get('player_name_2'))
    test = get_player_id(session.get('player_name_1'))
    test2 = get_player_id(session.get('player_name_2'))
    print("Reached after get_player_id")
    session['player_id1'] = test
    session['player_id2'] = test2


    # if 'player_id' not in data:
    #    return jsonify({})

    return render_template('index.html', user_id1=session.get['player_id1'], user_id2=session.get['player_id2'])


def get_player_id(username):
    print("Reached get_player_id")
    url = 'https://open.faceit.com/data/v4/players?nickname={}'.format(username)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + app.api_key
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if 'player_id' not in data:
        return jsonify({})

    player_id = data['player_id']
    print(player_id)
    return jsonify({'player_id': player_id})


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    player1_id = session.get('player1')
    player2_id = session.get('player2')

    if not player1_id or not player2_id:
        return jsonify({})

    if data['player_id'] in [player1_id, player2_id]:
        payload = {
            'match_id': data['entity']['match_id'],
            'player_id': data['player_id']
        }

        if player1_id == data['player_id']:
            player1_payloads = session.get(player1_id, [])
            player1_payloads.append(payload)
            session[player1_id] = player1_payloads
        else:
            player2_payloads = session.get(player2_id, [])
            player2_payloads.append(payload)
            session[player2_id] = player2_payloads

    return jsonify({})


@app.route('/compare-payloads', methods=['POST'])
def compare():
    data = request.get_json()
    user_id_1 = session.get("user_id_1")
    user_id_2 = session.get("user_id_2")

    if not user_id_1 or not user_id_2:
        return redirect("/")

    player1_payloads = session.get(player1_id)
    player2_payloads = session.get(player2_id)

    if not player1_payloads or not player2_payloads:
        return jsonify([])

    player1_match_ids = set([payload['match_id'] for payload in player1_payloads])
    player2_match_ids = set([payload['match_id'] for payload in player2_payloads])

    common_match_ids = player1_match_ids.intersection(player2_match_ids)

    return jsonify(list(common_match_ids))


if __name__ == '__main__':
    app.run(debug=True)
