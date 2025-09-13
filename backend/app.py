import requests, random, os
from flask import Flask, render_template, jsonify
from datetime import datetime, date
from flask_cors import CORS

app = Flask(__name__,
                    template_folder="../frontend/templates",
                    static_folder="../frontend/static")
CORS(app)

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
    layout = data["layout"]

    # Check card against vars, returning either card, scryfall_url or None, None
    if "Creature" not in typ and "can be your commander" not in oracle:
        print("NOT A LEGAL CMDR CARD!!!")
        return None, None
    elif set_name in {"ugl" , "unh" , "ust" , "und" , "unf"}:
        print("UN-SET!!!")
        return None, None
    elif release > today:
        print("NOT RELEASED YET!!!")
        return None, None
    print("NORMAL CARD")

    # Single-faced card
    if "image_uris" in data:
        card = data["image_uris"]["normal"]

    # Multi-faced card
    elif "card_faces" in data and layout != "transform":
        legal_faces = []

        for face in data["card_faces"]:
            type_line = face.get("type_line", "")
            oracle = face.get("oracle_text", "")

            # Check if this face is commander-legal
            if "Legendary Creature" in type_line or "can be your commander" in oracle:
                if "image_uris" in face:
                    legal_faces.append(face["image_uris"]["normal"])

        if legal_faces:
            # Pick a random legal face
            card = random.choice(legal_faces)
        else:
            # fallback: pick first face image if no legal face found
            if data["card_faces"][0].get("image_uris"):
                card = data["card_faces"][0]["image_uris"]["normal"]
            else:
                print("NO IMAGE FOUND!!!")
                return None, None

    else:
        print("NO IMAGE FOUND!!!")
        return None, None

    return card, data.get("scryfall_uri")

def get_random_partner():
    # Inital API call to scryfall
    api_url = "https://api.scryfall.com/cards/random?q=is:commander+o:\"Partner\"+-o:\"Partner with\"+game:paper"
    response = requests.get(api_url)
    data = response.json()

    # Set vars for distunguishing illegal cmdrs
    print("URL:", data["scryfall_uri"])
    typ = data["type_line"]
    oracle = data.get("oracle_text", "")
    set_name = data["set"]
    release =  datetime.strptime(data["released_at"], "%Y-%m-%d").date()
    today = date.today()

    # Check card against vars, returning either card, scryfall_url or None, None
    if "Creature" not in typ and "can be your commander" not in oracle:
        print("NOT A LEGAL CMDR CARD!!!")
        return None, None
    elif set_name in {"ugl" , "unh" , "ust" , "und" , "unf"}:
        print("UN-SET!!!")
        return None, None
    elif release > today:
        print("NOT RELEASED YET!!!")
        return None, None
    else:
        print("NORMAL PARTNER")
        card = data["image_uris"]["normal"]
        return card, data["scryfall_uri"]

def get_random_bkgr_cmdr():
    # Inital API call to scryfall
    api_url = "https://api.scryfall.com/cards/random?q=is:commander+o:\"Choose a background\"+game:paper"
    response = requests.get(api_url)
    data = response.json()

    # Set vars for distunguishing illegal cmdrs
    print("URL:", data["scryfall_uri"])
    set_name = data["set"]
    release =  datetime.strptime(data["released_at"], "%Y-%m-%d").date()
    today = date.today()

    # Check card against vars, returning either card, scryfall_url or None, None
    if set_name in {"ugl" , "unh" , "ust" , "und" , "unf"}:
        print("UN-SET!!!")
        return None, None
    elif release > today:
        print("NOT RELEASED YET!!!")
        return None, None
    else:
        print("NORMAL BACKGROUND COMMANDER")
        card = data["image_uris"]["normal"]
        return card, data["scryfall_uri"]

def get_random_bkgr():
    # Inital API call to scryfall
    api_url = "https://api.scryfall.com/cards/random?q=is:commander+t:legendary+t:background+game:paper"
    response = requests.get(api_url)
    data = response.json()

    # Set vars for distunguishing illegal cmdrs
    print("URL:", data["scryfall_uri"])
    set_name = data["set"]
    release =  datetime.strptime(data["released_at"], "%Y-%m-%d").date()
    today = date.today()

    # Check card against vars, returning either card, scryfall_url or None, None
    if set_name in {"ugl" , "unh" , "ust" , "und" , "unf"}:
        print("UN-SET!!!")
        return None, None
    elif release > today:
        print("NOT RELEASED YET!!!")
        return None, None
    else:
        print("NORMAL BACKGROUND")
        card = data["image_uris"]["normal"]
        return card, data["scryfall_uri"]

@app.route('/', methods = ["GET"])
def cmdr():
    card_url = get_random_card()
    partner_1_url = get_random_partner()
    partner_2_url = get_random_partner()
    bkgr_cmdr = get_random_bkgr_cmdr()
    bkgr = get_random_bkgr()

    # Log msgs for Render
    print("Hello from WhatsMyCommander on Render")
    
    return render_template('index.html', 
                            card_url=card_url, 
                            partner_1_url=partner_1_url, 
                            partner_2_url=partner_2_url,
                            bkgr_cmdr=bkgr_cmdr,
                            bkgr=bkgr
                            )

@app.route("/get-card")
def get_card():
    card_url, scryfall_url = get_random_card()
    while card_url is None or scryfall_url is None:
        card_url, scryfall_url = get_random_card()

    # Log msgs for Render
    print("Card fetched:", scryfall_url)

    return jsonify({"card_url": card_url, "scryfall_url": scryfall_url})

@app.route("/get-partner")
def get_partner():
    partner_1_url, partner_1_scryfall = get_random_partner()
    partner_2_url, partner_2_scryfall = get_random_partner()
    while partner_1_url is None or partner_1_scryfall is None or partner_2_url is None or partner_2_scryfall is None:
        partner_1_url, partner_1_scryfall = get_random_partner()
        partner_2_url, partner_2_scryfall = get_random_partner()
    
    # Log msgs for Render
    print("Partners fetched:", partner_1_scryfall, partner_2_scryfall)

    return jsonify({"partner_1_url": partner_1_url, 
                    "partner_1_scryfall": partner_1_scryfall, 
                    "partner_2_url": partner_2_url, 
                    "partner_2_scryfall":partner_2_scryfall
                    })

@app.route("/get-bkgr")
def get_bkgr():
    bkgr_cmdr, bkgr_cmdr_scryfall = get_random_bkgr_cmdr()
    bkgr, bkgr_scryfall = get_random_bkgr()
    while bkgr_cmdr is None or bkgr_cmdr_scryfall is None or bkgr is None or bkgr_scryfall is None:
        bkgr_cmdr, bkgr_cmdr_scryfall = get_random_bkgr_cmdr()
        bkgr, bkgr_scryfall = get_random_bkgr()

    # Log msgs for Render
    print("Background cmdrs fetched:", bkgr_cmdr_scryfall, bkgr_scryfall)

    return jsonify({"bkgr_cmdr": bkgr_cmdr,
                    "bkgr_cmdr_scryfall": bkgr_cmdr_scryfall,
                    "bkgr":bkgr,
                    "bkgr_scryfall": bkgr_scryfall
                    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)