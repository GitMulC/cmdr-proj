import pytest
import requests

def test_scryfall_api():
    """
    GIVEN a specific scryfall api address
    WHEN api url is called using requests & converted to json
    THEN json can be predictably read to ensure api is working
    """
    url = "https://api.scryfall.com/cards/a25/50"
    response = requests.get(url)
    data = response.json()

    assert response.status_code == 200
    assert "id" in data
    assert data["id"] == "cca8eb95-d071-46a4-885c-3da25b401806"
    assert "name" in data
    assert data["name"] == "Counterspell"