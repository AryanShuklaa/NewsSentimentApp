# utils.py
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import spacy
from gtts import gTTS
from googletrans import Translator

# Load sentiment analysis pipeline (using a pre-trained transformer model)
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load spaCy English model
# Make sure to run: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

def fetch_news(company_name):
    """
    Fetch news articles related to a given company using Google News RSS feed.
    Returns a list of articles with title, summary, and link.
    """
    url = f"https://news.google.com/rss/search?q={company_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")[:10]  # Get first 10 articles
    articles = []
    for item in items:
        title = item.title.text
        link = item.link.text
        # Attempt to fetch summary from the article page (simple approach)
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.content, "html.parser")
        paragraphs = article_soup.find_all("p")
        summary = " ".join([p.get_text() for p in paragraphs[:3]])
        articles.append({"title": title, "summary": summary, "link": link})
    return articles

def analyze_sentiment(text):
    """
    Analyze sentiment of a given text.
    Returns the sentiment label (e.g., POSITIVE or NEGATIVE).
    """
    result = sentiment_pipeline(text)[0]
    return result["label"]

def extract_topics(text):
    """
    Use spaCy's NER to extract key topics from text.
    Only considers entities labeled as ORG, PRODUCT, or GPE.
    Returns up to three unique topics.
    """
    doc = nlp(text)
    topics = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE"]]
    return list(set(topics))[:3]

def generate_hindi_audio(text, output_filename="output.mp3"):
    """
    Translate text to Hindi and generate a TTS audio file.
    Returns the filename of the saved audio.
    """
    translator = Translator()
    translated_text = translator.translate(text, dest="hi").text
    tts = gTTS(translated_text, lang="hi")
    tts.save(output_filename)
    return output_filename
