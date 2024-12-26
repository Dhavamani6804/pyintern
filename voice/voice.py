from flask import Flask, render_template, request, jsonify
import pyttsx3
import speech_recognition as sr
import requests
import datetime

app = Flask(__name__)

engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    """Fetch weather data using OpenWeatherMap API."""
    API_KEY = "d52a870e486fceab78516aa4c5c7edef"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
        }
        return weather
    else:
        return None

def get_news():
    """Fetch top news headlines using NewsAPI."""
    API_KEY = "a00c83d645fc4c7197b8ad5c73a0f846"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        headlines = [article["title"] for article in articles[:5]]
        return headlines
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    result = {}
    if request.method == 'POST':
        command = request.form.get('command', '').lower()

        if "weather" in command:
            city = request.form.get('city', '')
            weather = get_weather(city)
            if weather:
                result = {
                    "response": f"The weather in {city} is {weather['description']} with a temperature of {weather['temperature']}°C and humidity of {weather['humidity']}%."
                }
            else:
                result = {"response": "Sorry, I couldn't fetch the weather."}

        elif "news" in command:
            news = get_news()
            if news:
                result = {
                    "response": "Here are the top 5 headlines: " + ", ".join(news)
                }
            else:
                result = {"response": "Sorry, I couldn't fetch the news."}

        elif "reminder" in command:
            reminder_text = request.form.get('reminder_text', '')
            if reminder_text:
                set_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
                result = {
                    "response": f"Reminder set for: {reminder_text}. I'll remind you in 10 seconds."
                }
                while datetime.datetime.now() < set_time:
                    pass
                speak(f"Reminder: {reminder_text}")
                result["response"] += " Reminder triggered!"
            else:
                result = {"response": "No reminder text provided."}

        elif "exit" in command:
            result = {"response": "Goodbye!"}

        else:
            result = {"response": "Sorry, I don't understand that command."}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
