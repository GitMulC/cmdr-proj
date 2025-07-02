import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def get_random_card():
    api_url = "https://api.scryfall.com/cards/random?q=is%3Acommander"
    response = requests.get(api_url)
    data = response.json()

    # print(data)
    print("URL:", data["uri"])
    games = data["games"]
    print("Games:", games)

    if len(games) == 1 and games[0] == "arena":
        print("ARENA ONLY CARD!!!")
        error_api_url = "https://api.scryfall.com/cards/61e9c6df-1c84-4eab-9076-a4feb6347c10"
        error_response = requests.get(error_api_url)
        error_data = response.json()
        error_card = data["image_uris"]["normal"]
        return error_card
    else:
        print("NORMAL CARD")
        card = data["image_uris"]["normal"]
        return card

@app.route('/', methods = ["GET"])
def cmdr():
    card_url = get_random_card()
    return render_template('index.html', card_url=card_url)

@app.route("/get-card")
def get_card():
    card_url = get_random_card()
    return jsonify({"card_url": card_url})


if __name__ == "__main__":
    app.run(debug=True)