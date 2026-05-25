from fastapi import FastAPI, HTTPException
import json
from ingestion import read_all_documents
from classify import classify_document
from extract import extract_fields
from vector_store import build_vectorstore, search_documents

app = FastAPI()

OUTPUT_FILE = "output.json"

@app.post("/process")
def process_documents():
    documents = read_all_documents("data")
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found in data/ folder.")

    results = {}

    for filename, text in documents.items():
        doc_class = classify_document(text)
        fields    = extract_fields(doc_class, text)
        results[filename] = {"class": doc_class, **fields}

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    docs_list = [{"filename": filename, "text": text} for filename, text in documents.items()]

    build_vectorstore(docs_list)

    return {
        "message":"Processing complete.",
        "processed_documents": len(results),
        "results": results}


@app.post("/search")
def search(q:str, top_k: int = 5):

    results = search_documents(q, top_k)
    if not results:
        raise HTTPException(status_code=404, detail="No results found.")

    return {"query":q, "results": results}