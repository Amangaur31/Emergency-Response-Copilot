# 🚑 Emergency Response Copilot (RAG + GenAI)

An AI-powered **Retrieval-Augmented Generation (RAG)** chatbot that provides real-time, accurate emergency response guidance by retrieving information from official SOP and legal PDF documents.

This system supports emergency scenarios such as **road accidents, fire incidents, floods, disaster management, and traffic law compliance**, generating structured step-by-step actions grounded in retrieved context.



## ✨ Key Features

- Emergency SOP-based Question Answering  
- Semantic Search over PDF Documents  
- Context-Grounded LLM Responses (Hallucination Controlled)  
- Step-by-Step Actionable Output Format  
- Streamlit Chatbot Interface  
- FastAPI Backend for Scalable Deployment  


## 🏗️ System Architecture

<img width="1536" height="1023" alt="image" src="https://github.com/user-attachments/assets/d7185045-1d29-40f2-a978-70ce9a6f0667" />




## 📌 Tech Stack

| Component        | Tool/Framework |
|-----------------|----------------|
| Frontend UI      | Streamlit |
| Backend API      | FastAPI |
| Vector Database  | ChromaDB |
| Embeddings       | HuggingFace MiniLM |
| LLM API          | Gemini / Groq |
| Document Source  | PDF SOP + Legal Docs |
| Deployment Ready | Render + Streamlit Cloud |


## 📂 Project Structure

```bash
Emergency-Response-Copilot/
│
├── app.py                    # Streamlit Chatbot UI
├── main.py                   # FastAPI Entry Point
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
│
├── rag/
│   ├── pipeline.py           # Full RAG workflow
│   ├── retriever.py          # Chroma similarity search
│   ├── llm.py                # LLM API integration
│   ├── chunking.py           # Chunking logic
│
├── data/
│   ├── sop_docs.pdf          # Emergency SOP reference docs
│
└── chroma_db/                # Persistent vector store
```




## ⚙️ How It Works (RAG Pipeline)

1. **PDF SOP documents** are ingested and chunked  
2. Each chunk is converted into embeddings using **MiniLM**  
3. Chunks are stored in **Chroma Vector DB**  
4. User query triggers semantic retrieval of top-k matches  
5. Retrieved context is passed into **Gemini/Groq LLM**  
6. Model generates a grounded emergency response answer  


## 🚀 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Emergency-Response-Copilot-RAG.git
cd Emergency-Response-Copilot-RAG
```
2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Add API Key
```bash
Create a .env file in root directory:

GEMINI_API_KEY=your_api_key_here
```
▶️ Run the Application
```
Start FastAPI Backend
uvicorn main:app --reload

Backend runs at:
http://127.0.0.1:8000

Start Streamlit Frontend
streamlit run app.py

App runs at:
http://localhost:8501
