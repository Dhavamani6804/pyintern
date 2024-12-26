from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    sentiment_data = None  s
    if request.method == 'POST':
        user_text = request.form.get('text')  
        if user_text:
            analysis = TextBlob(user_text)
            polarity = analysis.sentiment.polarity
            subjectivity = analysis.sentiment.subjectivity

            if polarity > 0:
                sentiment = "Positive"
            elif polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            sentiment_data = {
                "text": user_text,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "sentiment": sentiment,
            }
    return render_template('index.html', sentiment_data=sentiment_data)

if __name__ == '__main__':
    app.run(debug=True)
