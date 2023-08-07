import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')  # Get the API key from environment variables
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if data['cod'] == '404':
        return 'City not found. Please try again.'
    
    temp = data['main']['temp']
    return render_template('weather.html', city=city, temp=temp)

if __name__ == '__main__':
    app.run(debug=True)
