from flask import Flask, request

app = Flask(__name__)


@app.route('/comparison', methods=['POST'])
def compare_match_ids():
    data1 = request.get_json()
    data2 = request.get_json()

    if data1.get('match_id') == data2.get('match_id'):
        return 'Die Match-IDs sind identisch!'
    else:
        return 'Die Match-IDs sind unterschiedlich!'


if __name__ == '__main__':
    app.run()
