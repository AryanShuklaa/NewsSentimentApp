import streamlit as st
import requests
import json

st.set_page_config(page_title="News Summarization & Sentiment Analysis with Hindi TTS", layout="wide")
st.title("📰 News Summarization & Sentiment Analysis with Hindi TTS")
st.write("Enter a company name to fetch and analyze recent news articles.")

company_name = st.text_input("Enter Company Name", "")

if st.button("Analyze"):
    if company_name.strip():
        st.info("Fetching and analyzing news, please wait...")
        API_URL = "http://127.0.0.1:8000/analyze/"
        try:
            response = requests.post(API_URL, json={"company": company_name})
            response.raise_for_status()
            data = response.json()
            st.subheader(f"News Analysis for {data['company']}")

            # Comparative Sentiment Analysis
            comp = data.get("comparative_sentiment", {})
            st.write("### Comparative Sentiment Analysis")
            st.write("Sentiment Distribution:", comp.get("sentiment_distribution", {}))
            st.write("Overall Sentiment:", comp.get("overall_sentiment", "N/A"))
            st.markdown("---")

            # Display Articles
            for idx, article in enumerate(data["articles"], start=1):
                st.write(f"### News {idx}")
                st.write(f"**Title:** {article['title']}")
                st.write(f"**Summary:** {article['summary']}")
                st.write(f"**Sentiment:** {article['sentiment']} (Confidence: {article['confidence']:.2f})")
                st.markdown(f"[Read more]({article['url']})")

                # Audio Player & Download Button (Unique Keys Added)
                if article.get("tts_file"):
                    st.audio(article["tts_file"], format="audio/mp3")
                    with open(article["tts_file"], "rb") as f:
                        st.download_button(
                            "Download Hindi Audio",
                            f,
                            file_name=article["tts_file"],
                            key=f"download_{idx}"
                        )
                st.markdown("---")
        except requests.exceptions.HTTPError as http_err:
            st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as req_err:
            st.error(f"Connection Error: {req_err}")
        except json.JSONDecodeError:
            st.error("Invalid JSON response from API.")
    else:
        st.error("Please enter a valid company name.")
