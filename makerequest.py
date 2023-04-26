from flask import Flask, request, jsonify, session
import requests
import json

api_key = "bbc65b04-9802-42d1-889d-9b52f1b42166"


def getPlayerIDfromUsername(username):
    # Set API endpoint and parameters
    url = "https://open.faceit.com/data/v4/players?nickname={}".format(username)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        player_id = data["player_id"]
        print(f"The player ID for {username} is: {player_id}")
        return player_id
    else:
        print(f"Failed to get player ID for {username}. Status code: {response.status_code}")
        return "Player not found - Status code: {}".format(response.status_code)


def makeRequest(api_url, player_id):
    # Set API endpoint and parameters
    category = "players"
    thisplayer_id = "{}".format(player_id)  # Replace with your player ID
    game = "csgo"
    region = "EU"

    # Set headers with API key
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer bbc65b04-9802-42d1-889d-9b52f1b42166"  # Replace with your API key
    }

    # Send GET request to API endpoint with parameters
    # response = requests.get(f"{api_url}/{category}/{player_id}/stats/{game}", headers=headers)
    response = requests.get(f"{api_url}/{category}/{thisplayer_id}/history", headers=headers)

    # Parse JSON response
    thisjson_data = json.loads(response.text)
    # json_data2 = json.loads(response2.text)
    return thisjson_data  # , json_data2


# player_id = getPlayerID()
# json_data = makeRequest()
# Print player stats
#print(json_data)
#print(player_id)
# print(json_data["lifetime"])
