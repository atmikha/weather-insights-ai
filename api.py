
import requests


def get_weather_data():
    """Fetch historical daily weather data for Bloomington, Indiana."""

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": 39.1653,
        "longitude": -86.5264,
        "start_date": "2025-10-01",
        "end_date": "2025-10-07",
        "daily": "temperature_2m_max,precipitation_sum",
        "timezone": "America/Indiana/Indianapolis",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    data = get_weather_data()
    print(data["daily"])
