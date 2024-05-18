from flask import Flask, request, jsonify
from flask_cors import CORS  # Flask-CORS kütüphanesini import et
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from mtranslate import translate
import requests

import nltk
nltk.download('vader_lexicon')
app = Flask(__name__)
CORS(app)  # Flask uygulamasına CORS desteğini ekleyin

class WebScraper:
    def __init__(self):
        pass

    def scrape_comment(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = soup.find_all('div', class_='message-content js-messageContent')
        comments_list = []
        for comment in comments:
            comment_link = comment.find('div', class_='bbWrapper')
            if comment_link:
                comments_list.append(comment_link.text.strip())
        return comments_list

def analyze_sentiment(comments):
    sid = SentimentIntensityAnalyzer()
    analyzed_complaints = []
    for comment in comments:
        scores = sid.polarity_scores(comment)
        if scores['compound'] > 0.05:
            analyzed_complaints.append((comment, "Positive"))
        elif scores['compound'] < -0.05:
            analyzed_complaints.append((comment, "Negative"))
        else:
            analyzed_complaints.append((comment, "Neutral"))
    return analyzed_complaints

def translate_to_english(texts):
    translations = []
    for text in texts:
        translation = translate(text, 'en')
        translations.append(translation)
    return translations

@app.route('/url', methods=['POST'])
def process_url():
    data = request.get_json()
    url = data['url']
    scraper = WebScraper()
    comments = scraper.scrape_comment(url)
    translations = translate_to_english(comments)
    sentiments = analyze_sentiment(translations)

    # Çıktıyı oluştur
    output = ""
    for complaint, sentiment in sentiments:
        output += "Şikayet: " + complaint + "\n"
        output += "Duygu Durumu: " + sentiment + "\n"
        output += "--------------\n"

    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(debug=True)
