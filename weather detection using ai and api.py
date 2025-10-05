from flask import Flask, jsonify
import requests

API_KEY = "f6172a9e9794ddac2b0626f48fcfe466"
CITY = "Bhubaneswar"

WEATHER_SPEED_LIMIT = {
    "Rain": 50,
    "Fog": 30,
    "Mist": 60,
    "Thunderstorm": 40,
    "Drizzle": 45,
    "Snow": 25,
    "Haze": 55
}

DEFAULT_SPEED_LIMIT = 65

app = Flask(__name__)

def get_weather_data():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return {
                "weather": "Error",
                "temperature": "N/A",
                "speed_limit": "N/A",
                "message": data.get("message", "Unknown error")
            }

        main_weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        speed_limit = WEATHER_SPEED_LIMIT.get(main_weather, DEFAULT_SPEED_LIMIT)

        return {
            "weather": main_weather,
            "temperature": temp,
            "speed_limit": speed_limit
        }

    except Exception as e:
        return {
            "weather": "Error",
            "temperature": "N/A",
            "speed_limit": "N/A",
            "message": str(e)
        }

@app.route('/weather', methods=['GET'])
def weather():
    weather_info = get_weather_data()
    return jsonify(weather_info)

if __name__ == "__main__":
    print("[INFO] Starting Flask Weather JSON server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
