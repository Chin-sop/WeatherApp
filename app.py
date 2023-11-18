import os
import requests
import json
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Index route, renders the index.html template when accessed at the root URL
@app.route('/')
def index():
    return render_template('index.html')

# Weather route, renders the weather.html template with the current weather data
# for the city entered by the user
@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city'] # Get the city name from the submitted form
    api_key = os.getenv('OPENWEATHERMAP_API_KEY') # Get the API key from the .env file
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}' # Construct the API request URL
    response = requests.get(url)
    
    data = response.json()

    if data['cod'] != '404': # If the city is found
        weather = data['weather'][0]['main'] # Get the main weather description
        description = data['weather'][0]['description'] # Get the detailed weather description
        temperature = data['main']['temp'] # Get the current temperature
        feels_like = data['main']['feels_like'] # Get the temperature feeling
        humidity = data['main']['humidity'] # Get the current humidity
        wind_speed = data['wind']['speed'] # Get the current wind speed
        pressure = data['main']['pressure'] # Get the current pressure
        sunrise = data['sys']['sunrise'] # Get the current sunrise time
        sunset = data['sys']['sunset'] # Get the current sunset time

        return render_template('weather.html', city=city, weather=weather, description=description, temperature=temperature, feels_like=feels_like, humidity=humidity, wind_speed=wind_speed, pressure=pressure, sunrise=sunrise, sunset=sunset) # Render the weather.html template with the current weather data
        
    else:
        return 'City not found. Please try again.' # Return an error message if the city is not found


    
if __name__ == '__main__':
    app.run(debug=True)