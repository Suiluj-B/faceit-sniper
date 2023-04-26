from flask import Flask, render_template, session
import json
import time

import executeer


# Define a route to display the received data on a website
@executeer.app.route('/sniping', methods=['POST'])
def snipe():
    print('Testing')
    data1 = load_json('a1cd9f03-faaf-42b4-8c4e-2f61a9b5bce6.json')
    data2 = load_json('51195669-ffa8-4386-93e8-57d80ba22e0a.json')
    session['last_update_to_file_1'] = data1.get('received at:')
    session['last_update_to_file_2'] = data2.get('received at:')
    revalidate_file()
    return render_template('sniping.html', sniping_status=session['sniping_status'])


@executeer.app.before_request
def before_request():
    executeer.run_sniper()


@executeer.app.template_filter('sniping_status')
def get_sniping_status():
    return session['sniping_status']


def revalidate_file():
    # Retrieve the stored data from your database or other data storage system
    print('Revalidating the files')
    data1 = load_json('a1cd9f03-faaf-42b4-8c4e-2f61a9b5bce6.json')
    data2 = load_json('51195669-ffa8-4386-93e8-57d80ba22e0a.json')
    # data1 = load_json('{}.json'.format(session.get('user_id_1')))
    # data2 = load_json('{}.json'.format(session.get('user_id_2')))
    # Compare the match IDs
    session.updated = False
    if data1.get('received at:') != session['last_update_to_file_1'] and data2.get('received at:') != session[
        'last_update_to_file_2']:
        session.updated = True
        print('File 1 has not been updated')

    if session.updated:
        if data1.get('match_id') == data2.get('match_id'):
            session['sniping_status'] = 'Die Match-IDs sind identisch!'
        else:
            session['sniping_status'] = 'Die Match-IDs sind unterschiedlich!'
    else:
        session['sniping_status'] = 'Warte auf neue Match_IDs...'

    return render_template('sniping.html', sniping_status=session['sniping_status'])


def save_json(payload, filename):
    with open(filename, 'w') as f:
        json.dump(payload, f)


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


# Start the server and listen on a port
if __name__ == '__main__':
    app.run(debug=True, port=5000)
