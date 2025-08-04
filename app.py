import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def get_random_card():
    # Inital API call to scryfall
    api_url = "https://api.scryfall.com/cards/random?q=is%3Acommander"
    response = requests.get(api_url)
    data = response.json()

    # Set vars for distunguishing illegal cmdrs
    print("URL:", data["uri"])
    games = data["games"]
    typ = data["type_line"]
    oracle = data.get("oracle_text", "")
    set_name = data["set"]

    # Setup error card, mental misstep for illegal cmdrs for comparisson later
    error_api_url = "https://api.scryfall.com/cards/61e9c6df-1c84-4eab-9076-a4feb6347c10"
    error_response = requests.get(error_api_url)
    error_data = error_response.json()
    error_card = error_data["image_uris"]["normal"]

    # Check card against vars, returning either card or error_card
    if len(games) == 1 and games[0] == "arena":
        print("ARENA ONLY CARD!!!")
        return error_card
    elif len(games) == 1 and games[0] == "mtgo":
        print("MTGO ONLY CARD!!!")
        return error_card
    elif "Creature" not in typ and "can be your commander" not in oracle:
        print("NOT A LEGAL CMDR CARD!!!")
        return error_card
    elif set_name in {"ugl" , "unh" , "ust" , "und" , "unf"}:
        print("UN-SET!!!")
        return error_card
    else:
        print("NORMAL CARD")
        if "image_uris" in data:
            card = data["image_uris"]["normal"]
        elif "card_faces" in data and data["card_faces"][0].get("image_uris"):
            card = data["card_faces"][0]["image_uris"]["normal"]
        else:
            print("NO IMAGE FOUND - returning error card")
            return error_card
        return card

@app.route('/', methods = ["GET"])
def cmdr():
    card_url = get_random_card()
    return render_template('index.html', card_url=card_url)

@app.route("/get-card")
def get_card():
    card_url = get_random_card()
    print(card_url)
    while card_url == "https://cards.scryfall.io/normal/front/6/1/61e9c6df-1c84-4eab-9076-a4feb6347c10.jpg?1566819829":
        card_url = get_random_card()
    return jsonify({"card_url": card_url})


if __name__ == "__main__":
    app.run(debug=True)