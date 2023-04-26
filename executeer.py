from flask import Flask, request, jsonify, render_template, session
import makerequest
import match_id_comparer
import webhooks_receiver
import sniping
import time

app = Flask(__name__)
api_key = "bbc65b04-9802-42d1-889d-9b52f1b42166"
nickname = "Jodokus"
app.secret_key = 'super secret key'


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/home', methods=['POST'])
def process_form():
    print('Process_form was called')
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    session['player_name_1'] = request.form['player_name_1']
    session['player_name_2'] = request.form['player_name_2']
    session['user_id_1'] = makerequest.getPlayerIDfromUsername(request.form['player_name_1'])
    session['user_id_2'] = makerequest.getPlayerIDfromUsername(request.form['player_name_2'])
    return render_template('index.html', user_id_1=session['user_id_1'], user_id_2=session['user_id_2'])


@app.context_processor
def inject_player_ids():
    print('Injecting player IDs')
    return dict(player_id_1=session.get('user_id_1'), player_id_2=session.get('user_id_2'))


@app.route('/sniping', methods=['POST'])
def goto_sniping():
    r = sniping.snipe()
    return r


def run_sniper():
    w = sniping.revalidate_file()
    if session.updated == True:
        print('The files have been updated')
    else:
        print('The files have not been updated')
        time.sleep(2)
        run_sniper()
    return w


@app.route('/webhook', methods=['POST'])
def webhooks():
    r = webhooks_receiver.handle_webhook()
    return r


if __name__ == '__main__':
    app.run(debug=True, port=5000)
