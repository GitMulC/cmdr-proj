import requests
from flask import Flask, render_template, jsonify
from datetime import datetime, date

app = Flask(__name__)

def get_random_card():
    # Inital API call to scryfall
    api_url = "https://api.scryfall.com/cards/random?q=is%3Acommander+game%3Apaper"
    response = requests.get(api_url)
    data = response.json()

    # Set vars for distunguishing illegal cmdrs
    print("URL:", data["scryfall_uri"])
    games = data["games"]
    typ = data["type_line"]
    oracle = data.get("oracle_text", "")
    set_name = data["set"]
    release =  datetime.strptime(data["released_at"], "%Y-%m-%d").date()
    today = date.today()

    # Check card against vars, returning either card, scryfall_url or None, None
    if len(games) == 1 and games[0] == "arena":
        print("ARENA ONLY CARD!!!")
        return None, None
    elif len(games) == 1 and games[0] == "mtgo":
        print("MTGO ONLY CARD!!!")
        return None, None
    elif "Creature" not in typ and "can be your commander" not in oracle:
        print("NOT A LEGAL CMDR CARD!!!")
        return None, None
    elif set_name in {"ugl" , "unh" , "ust" , "und" , "unf"}:
        print("UN-SET!!!")
        return None, None
    elif release > today:
        print("NOT RELEASED YET!!!")
        return None, None
    else:
        print("NORMAL CARD")
        if "image_uris" in data:
            card = data["image_uris"]["normal"]
        elif "card_faces" in data and data["card_faces"][0].get("image_uris"):
            card = data["card_faces"][0]["image_uris"]["normal"]
        else:
            print("NO IMAGE FOUND!!!")
            return None, None
        return card, data["scryfall_uri"]

@app.route('/', methods = ["GET"])
def cmdr():
    card_url = get_random_card()
    return render_template('index.html', card_url=card_url)

@app.route("/get-card")
def get_card():
    card_url, scryfall_url = get_random_card()
    while card_url is None or scryfall_url is None:
        card_url, scryfall_url = get_random_card()
    return jsonify({"card_url": card_url, "scryfall_url": scryfall_url})


if __name__ == "__main__":
    app.run(debug=True)