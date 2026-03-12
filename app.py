from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your WeatherAPI key
API_KEY = "8854b73bcc7b4e1d861183328261203"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        # Current weather API
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        # Forecast API (5-day)
        forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=5&aqi=no&alerts=no"

        try:
            weather_response = requests.get(weather_url).json()
            forecast_response = requests.get(forecast_url).json()

            # Check if current weather returned an error
            if "error" in weather_response:
                error = weather_response["error"].get("message", "Error fetching weather data")
            else:
                weather = weather_response

            # Check forecast
            if "error" in forecast_response:
                if not error:
                    error = forecast_response["error"].get("message", "Error fetching forecast data")
                forecast = []
            else:
                # Get the forecast list (one entry per day)
                forecast = forecast_response["forecast"]["forecastday"]

        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template("index.html", weather=weather, forecast=forecast, error=error)

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns this automatically
    app.run(host="0.0.0.0", port=port, debug=True)