from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "d52a870e486fceab78516aa4c5c7edef"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city')  
        if city:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    weather_data = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "weather": data["weather"][0]["description"].capitalize(),
                        "icon": data["weather"][0]["icon"],
                    }
                else:
                    error_message = f"City '{city}' not found. Please try again."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
        else:
            error_message = "City name cannot be empty."

    return render_template('index.html', weather=weather_data, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
