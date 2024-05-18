
from flask import Flask, request, jsonify
<<<<<<< HEAD
from flask_cors import CORS
=======
from flask_cors import CORS  # Flask-CORS kütüphanesini import et
>>>>>>> e018ae1 (Add files via upload)
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from mtranslate import translate
import requests

import nltk
nltk.download('vader_lexicon')
<<<<<<< HEAD

app = Flask(__name__)
CORS(app)
=======
app = Flask(__name__)
CORS(app)  # Flask uygulamasına CORS desteğini ekleyin
>>>>>>> e018ae1 (Add files via upload)

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
<<<<<<< HEAD
    positive_count = 0
    negative_count = 0
=======
>>>>>>> e018ae1 (Add files via upload)
    for comment in comments:
        scores = sid.polarity_scores(comment)
        if scores['compound'] > 0.05:
            analyzed_complaints.append((comment, "Positive"))
<<<<<<< HEAD
            positive_count += 1
        elif scores['compound'] < -0.05:
            analyzed_complaints.append((comment, "Negative"))
            negative_count += 1
        else:
            analyzed_complaints.append((comment, "Neutral"))
    total_comments = len(comments)
    positive_ratio = positive_count / total_comments if total_comments > 0 else 0
    negative_ratio = negative_count / total_comments if total_comments > 0 else 0
    return analyzed_complaints, positive_ratio, negative_ratio
=======
        elif scores['compound'] < -0.05:
            analyzed_complaints.append((comment, "Negative"))
        else:
            analyzed_complaints.append((comment, "Neutral"))
    return analyzed_complaints
>>>>>>> e018ae1 (Add files via upload)

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
<<<<<<< HEAD
    sentiments, positive_ratio, negative_ratio = analyze_sentiment(translations)
=======
    sentiments = analyze_sentiment(translations)
>>>>>>> e018ae1 (Add files via upload)

    # Çıktıyı oluştur
    output = ""
    for complaint, sentiment in sentiments:
        output += "Şikayet: " + complaint + "\n"
        output += "Duygu Durumu: " + sentiment + "\n"
        output += "--------------\n"
<<<<<<< HEAD
    
    output += f"Pozitif Duygu Oranı: {positive_ratio:.2f}\n"
    output += f"Negatif Duygu Oranı: {negative_ratio:.2f}\n"
=======
>>>>>>> e018ae1 (Add files via upload)

    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(debug=True)

