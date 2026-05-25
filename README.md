# AI Document Processor

A local AI system that ingests, classifies, extracts structured data from, and semantically searches PDF/TXT documents. Runs fully offline — no paid APIs used.

---

## Project Structure

```
ai_document_processor/
├── data/                ← Put your PDF and TXT files here
├── vectorstore/         ← Auto-generated after /process
│   ├── faiss.index      ← FAISS vector index
│   └── metadata.pkl     ← Document metadata
├── models/              ← Embedding model
├── main.py              ← FastAPI app (entry point)
├── ingest.py            ← Reads and cleans PDF/TXT files
├── classify.py          ← Classifies each document
├── extract.py           ← Extracts structured fields
├── vector_store.py      ← Builds and searches FAISS index
├── output.json          ← Generated results
└── README.md
```

---

## Installation

**1. Create a virtual environment**
```bash
python -m venv venv

source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**2. Install dependencies**
```bash
pip install fastapi uvicorn pypdf sentence-transformers faiss-cpu numpy
```

---

## How to Run

**1. Add your PDF or TXT files to the `data/` folder**

**2. Start the server**
```bash
uvicorn main:app --reload
```

**3. Open the interactive API docs**
```
http://localhost:8000/docs
```

---

## Endpoints

### `POST /process`
Reads all documents from `data/` folder, classifies each one, extracts structured fields, saves `output.json`, and builds the vector store.

---

### `POST /search`
Searches documents by meaning using semantic similarity.

**Request body:**
```json
{
  "query": "payments due in January",
  "top_k": 5
}
```