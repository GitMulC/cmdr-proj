# My MTG Commander Project

## Setup
1. Flask - venv
    * `cd backend/`
    * `source venv/bin/activate`
    * `python3 app.py`

2. Tailwind - CSS
    * `cd frontend/`
    * `npm install`
    * `npm run build:css`
    * `npx tailwindcss -i ./src/input.css -o ./static/css/style.css --minify` (For deployment, generates css & removes whitespaces)

3. Testing
    * `pytest -v` / `python3 -m pytest -v`
    * `python3 -m pytest tests`
    * `python3 -m pytest --last-failed`


### Sponsors
- Ko-Fi
- Buy Me a Coffee
- PayPal.me
- Stripe Payment Link

### References
- [Scryfall](https://scryfall.com/docs/api)
- [SVGs](https://github.com/Investigamer/mtg-vectors/tree/main) 