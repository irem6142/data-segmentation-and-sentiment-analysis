from webbrowser import Chrome
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from mtranslate import translate

class WebScraper:
    def __init__(self, url):
        self.url = url

    def scrape_Comment(self):
        response = requests.get(self.url)

        soup = BeautifulSoup(response.text, 'html.parser')

        comments = soup.find_all('div', class_='message-content js-messageContent')

        comments_list = []
        for comment in comments:
            comment_link = comment.find('div', class_='bbWrapper')
            if comment_link:
                comments_list.append(comment_link.text.strip())

        return comments_list

def analyze_sentiment(comments):
    # VaderSentimentIntensityAnalyzer sınıfını yükle
    sid = SentimentIntensityAnalyzer()

    # Şikayetlerin duygularını analiz et
    analyzed_complaints = []
    for comment in comments:
        # Duygu yoğunluğunu hesapla
        scores = sid.polarity_scores(comment)
        
        # Duygu durumuna göre etiket ekle
        if scores['compound'] > 0:
            analyzed_complaints.append((comment, "Pozitif"))
        elif scores['compound'] < 0:
            analyzed_complaints.append((comment, "Negatif"))
        else:
            analyzed_complaints.append((comment, "Nötr"))

    # Duygu analizi sonuçlarını döndür
    return analyzed_complaints


def translate_to_english(texts):
    translations = []
    for text in texts:
        translation = translate(text, 'en')
        translations.append(translation)
    return translations


# Chrome eklentisinden gelen mesajı al
def on_message(request, sender, send_response):
    if request.get('action') == 'getComments':
        url = request.get('url')
        scraper = WebScraper(url)
        comments = scraper.scrape_Comment()
        translations = translate_to_english(comments)
        sentiments = analyze_sentiment(translations)
        send_response({'comments': sentiments})

# Chrome eklentisine mesaj gönder
Chrome.runtime.onMessage.addListener(on_message)
