import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from transformers import pipeline
from gtts import gTTS
from googletrans import Translator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise Exception("NEWS_API_KEY is not set in the environment variables.")

NEWS_API_URL = "https://newsapi.org/v2/everything"

app = FastAPI()

# Request model
class NewsRequest(BaseModel):
    company: str

# Load NLP models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Translator for Hindi
translator = Translator()

def fetch_news(company: str):
    """Fetch news articles for the given company from NewsAPI."""
    params = {
        "qInTitle": company,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching news")

    data = response.json()
    if "articles" not in data or not isinstance(data["articles"], list) or len(data["articles"]) == 0:
        raise HTTPException(status_code=404, detail="No news articles found")
    
    return data["articles"]

def generate_hindi_tts(text: str, filename: str):
    """Translate text to Hindi and generate an MP3 file."""
    translation = translator.translate(text, dest="hi")
    hindi_text = translation.text
    tts = gTTS(text=hindi_text, lang="hi")
    tts.save(filename)
    return filename

def process_news(articles):
    """Process articles: summarize, analyze sentiment, and generate Hindi TTS."""
    processed = []
    for article in articles:
        title = article.get("title", "No Title")
        content = article.get("description") or article.get("content") or title
        if len(content.split()) < 5:
            continue  

        max_new_tokens = min(100, max(30, len(content.split()) // 2))
        min_length = max(10, max_new_tokens * 0.3)
        
        try:
            summary_output = summarizer(
                content,
                max_new_tokens=max_new_tokens,
                min_length=min_length,
                do_sample=False
            )
            summary = summary_output[0]["summary_text"]
        except Exception:
            summary = content[:200] + "..."

        sentiment_result = sentiment_analyzer(f"{title}. {summary}")[0]
        sentiment = sentiment_result["label"].capitalize()
        confidence = round(sentiment_result["score"], 2)

        filename = f"tts_{abs(hash(title)) % 100000}.mp3"
        try:
            generate_hindi_tts(summary, filename)
        except Exception:
            filename = ""

        processed.append({
            "title": title,
            "summary": summary,
            "sentiment": sentiment,
            "confidence": confidence,
            "url": article.get("url", "#"),
            "tts_file": filename
        })
    return processed

@app.post("/analyze/")
def analyze_news(request: NewsRequest):
    articles = fetch_news(request.company)
    processed_articles = process_news(articles)
    
    if not processed_articles:
        raise HTTPException(status_code=404, detail="No valid news articles processed")
    
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for art in processed_articles:
        sentiment_counts[art["sentiment"]] += 1
    overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    comparative_summary = (
        f"Overall sentiment is {overall_sentiment} "
        f"({sentiment_counts['Positive']} Positive, {sentiment_counts['Negative']} Negative, {sentiment_counts['Neutral']} Neutral articles)."
    )
    
    return {
        "company": request.company,
        "articles": processed_articles,
        "comparative_sentiment": {
            "sentiment_distribution": sentiment_counts,
            "overall_sentiment": comparative_summary
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
