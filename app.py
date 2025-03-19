import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def get_random_card():
    api_url = "https://api.scryfall.com/cards/random?q=is%3Acommander"
    response = requests.get(api_url)
    data = response.json()
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