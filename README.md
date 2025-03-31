# 📰 News Sentiment Analysis with Hindi Audio  

## 📌 Overview  
This project fetches **real-time news** articles for a given company, performs **sentiment analysis**, extracts **key topics**, and generates **Hindi audio summaries** using **FastAPI, Streamlit, Hugging Face NLP, spaCy, and Google TTS**.  

🚀 **Key Features:**  
✔ **Fetches news** from News API 
✔ **Performs sentiment analysis** using Hugging Face transformers  
✔ **Extracts key topics** using spaCy  
✔ **Generates Hindi speech summaries** using Google Translate & gTTS  
✔ **Interactive UI** with Streamlit  

---

## 🛠️ Tech Stack  
- **FastAPI** → Backend API  
- **Streamlit** → Frontend UI  
- **Hugging Face Transformers** → Sentiment Analysis (DistilBERT)  
- **spaCy** → Named Entity Recognition (Topic Extraction)  
- **Google Translate & gTTS** → Hindi audio generation  
- **BeautifulSoup & Requests** → Web scraping for news  

---

## ⚡ Quick Start (Run Locally)  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/your-username/news-sentiment-analysis.git
cd news-sentiment-analysis
2️⃣ Set Up a Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Run FastAPI (Backend)
bash
Copy
Edit
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
📌 FastAPI is now running at: http://127.0.0.1:8000

5️⃣ Run Streamlit (Frontend)
Open a new terminal and run:

bash
Copy
Edit
streamlit run app.py --server.port 8501 --server.address 127.0.0.1
📌 Streamlit is now available at: http://127.0.0.1:8501
