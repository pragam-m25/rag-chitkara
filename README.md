# rag-chitkara
# Chitkara RAG Assistant 🎓

An AI-powered **Retrieval-Augmented Generation (RAG)** assistant for answering questions from Chitkara University documents.

The system retrieves relevant information from university PDFs using **semantic search**, provides the retrieved context to **Gemini**, and generates an answer grounded in the available documents.

---

## 🚀 Features

* 📄 PDF document ingestion
* ✂️ Intelligent document chunking
* 🧠 Gemini embeddings for semantic search
* 🗄️ ChromaDB vector store
* 🔎 Similarity-based document retrieval
* 🤖 Gemini 2.5 Flash for answer generation
* 📚 Source document and page information
* ⚡ FastAPI backend
* 💬 Interactive web-based chat interface
* 🛡️ Context-grounded responses
* ❌ Avoids answering from general model knowledge when information is unavailable

---

## 🏗️ Architecture

```text
                    Chitkara University PDFs
                              │
                              ▼
                         ingest.py
                              │
                              ▼
                    PDF Document Loader
                              │
                              ▼
                   Recursive Text Splitter
                              │
                              ▼
                  Gemini Embedding Model
                              │
                              ▼
                         ChromaDB
                              │
                              │
                    ┌─────────▼─────────┐
                    │                   │
                    │     FastAPI       │
                    │     Backend       │
                    │                   │
                    └─────────┬─────────┘
                              │
                         User Question
                              │
                              ▼
                          Retriever
                              │
                              ▼
                    Relevant Documents
                              │
                              ▼
                       Context Builder
                              │
                              ▼
                         Prompt + Context
                              │
                              ▼
                      Gemini 2.5 Flash
                              │
                              ▼
                     Answer + Sources
                              │
                              ▼
                         Web Frontend
```

---

## 🛠️ Tech Stack

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Backend and RAG pipeline     |
| LangChain  | RAG orchestration            |
| Gemini     | Embeddings and LLM           |
| ChromaDB   | Vector storage and retrieval |
| FastAPI    | REST API                     |
| Pydantic   | Request validation           |
| HTML       | Frontend structure           |
| CSS        | Frontend styling             |
| JavaScript | Frontend interaction         |

---

## 📁 Project Structure

```text
rag-chitkara/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── ingest.py
├── main.py
├── README.md
├── .gitignore
└── .env
```

### Important local directories

```text
data/
```

Contains the university PDF documents used for ingestion.

```text
chroma_db/
```

Contains the locally generated ChromaDB vector store.

These directories are intentionally excluded from GitHub through `.gitignore`.

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone https://github.com/pragam-m25/rag-chitkara.git
```

```bash
cd rag-chitkara
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
```

The `.env` file should **never be committed to GitHub**.

---

# 📚 Document Ingestion

Place the university PDF documents inside:

```text
data/
```

Then run:

```bash
python ingest.py
```

The ingestion pipeline performs:

```text
PDFs
 ↓
Document Loading
 ↓
Text Splitting
 ↓
Chunk Creation
 ↓
Gemini Embeddings
 ↓
ChromaDB
```

The resulting vector database is stored locally in:

```text
chroma_db/
```

---

# 🧠 RAG Pipeline

When a user asks a question:

```text
User Question
      ↓
Retriever
      ↓
Top 4 Relevant Chunks
      ↓
Context Construction
      ↓
Prompt
      ↓
Gemini 2.5 Flash
      ↓
Grounded Answer
```

The current retriever uses:

```python
search_kwargs={"k": 4}
```

which retrieves the four most relevant chunks for a query.

---

# 🔌 FastAPI Backend

Start the backend using:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoint

### `POST /ask`

Request:

```json
{
  "question": "What is the course code of Object Oriented Programming?"
}
```

Example response:

```json
{
  "question": "What is the course code of Object Oriented Programming?",
  "answer": "The course code for Object Oriented Programming is 25CSE0204.",
  "sources": [
    {
      "document": "data/CHO_OOP_25CSE0204_B2025_3Sem_AIML.pdf",
      "page": "1"
    }
  ]
}
```

---

# 💻 Frontend

The frontend is located inside:

```text
frontend/
```

Start a local frontend server:

```bash
cd frontend
python -m http.server 5501
```

Then open:

```text
http://127.0.0.1:5501
```

The frontend communicates with the FastAPI backend through:

```text
POST http://127.0.0.1:8000/ask
```

---

# 🔄 Complete System Flow

```text
                    USER
                     │
                     ▼
              Web Chat Interface
                     │
                     │ POST /ask
                     ▼
                 FastAPI
                     │
                     ▼
                RAG Pipeline
                     │
              ┌──────┴──────┐
              ▼             ▼
          Retriever      Question
              │
              ▼
           ChromaDB
              │
              ▼
      Relevant PDF Chunks
              │
              ▼
          Context
              │
              ▼
        Gemini 2.5 Flash
              │
              ▼
       Answer + Sources
              │
              ▼
          Web Interface
```

---

# 🎯 Example Questions

The assistant can answer questions such as:

```text
What is the course code of Database Management System?

What is the course code of Object Oriented Programming?

What is the attendance requirement?

What are the objectives of the DBMS course?

What are the course learning outcomes?
```

The quality of answers depends on the documents available in the local knowledge base.

---

# 🛡️ Grounded Response Policy

The assistant is instructed to answer using the retrieved document context.

It is explicitly instructed:

```text
Answer the question using ONLY the provided context.

Do not use your own knowledge.

Do not infer missing facts.

Do not combine unrelated information to create an answer.

If the context does not contain enough information,
clearly say that the information was not found
in the available Chitkara documents.
```

This helps reduce unsupported or hallucinated answers.

---

# 🔐 Security

The following files/directories are excluded from version control:

```text
.env
.venv/
chroma_db/
data/
```

The Google API key must be stored in `.env` and should never be exposed publicly.

---

# 🚧 Current Limitations

This is an initial working version of the Chitkara RAG Assistant.

Current limitations include:

* Knowledge is limited to the ingested documents.
* Retrieval currently uses a fixed top-k value.
* No conversation memory yet.
* No authentication system.
* Documents currently need to be ingested manually.
* The vector database is currently local.
* Frontend and backend currently run separately during development.

---

# 🔮 Future Improvements

Possible next improvements include:

### Better Retrieval

* Hybrid search
* Metadata filtering
* Reranking
* Improved chunking strategies
* Query rewriting

### Better User Experience

* Chat history
* Streaming responses
* Better source cards
* Clickable source documents
* Loading and error states
* Mobile optimization

### University Features

* Course-wise filtering
* Department filtering
* Semester filtering
* Faculty information
* Academic calendar search
* Examination information
* Timetable-related queries

### Production Deployment

```text
Local Development
       ↓
Cloud Deployment
       ↓
Production Vector Database
       ↓
Production FastAPI
       ↓
University Web Application
```

---

# 📌 Project Status

**Current Status: Working Prototype / MVP**

The current implementation successfully demonstrates:

* PDF ingestion
* Document chunking
* Embedding generation
* Vector storage
* Semantic retrieval
* LLM-based answer generation
* FastAPI API
* Web frontend
* Source attribution

---

# 👨‍💻 Author

**Pragam**

Computer Science & Engineering — AI/ML

GitHub:
https://github.com/pragam-m25

---

## ⭐ Goal

The long-term goal of this project is to build a reliable AI knowledge assistant that can help Chitkara University students quickly access information from official university documents through natural-language questions.
