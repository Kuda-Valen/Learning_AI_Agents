
def get_weather(location: str, unit: str = "celcius") -> dict:
    mock_database = {
        "cape town": {"temperature": 18, "condition": "Sunny", "humidity": "60%"},
        "tokyo": {"temperature": 12, "condition": "Rainy", "humidity": "85%"},
        "london": {"temperature": 10, "condition": "cloudy", "humidity": "75%"}
    }

    loc_key = location.lower()
    data = mock_database.get(loc_key, {"temperature": 20, "condition": "clear", "humodity": "50%"})
    data["locatoin"] = location
    data["unit"] = unit
    return data