from pathlib import Path
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

VECTORSTORE_FOLDER = "vectorstore"
INDEX_PATH = "vectorstore/faiss.index"
METADATA_PATH = "vectorstore/metadata.pkl"
LOCAL_MODEL_PATH = "./models/all-MiniLM-L6-v2"
HF_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

if not os.path.exists(LOCAL_MODEL_PATH):
    print("Downloading model for the first time...")
    model = SentenceTransformer(HF_MODEL_NAME)
    os.makedirs(LOCAL_MODEL_PATH, exist_ok=True)
    model.save(LOCAL_MODEL_PATH)
    print(f"Model saved to {LOCAL_MODEL_PATH}")
else:
    print("Loading model from local cache...")
    model = SentenceTransformer(LOCAL_MODEL_PATH)


def build_vectorstore(documents: list[dict]):
    Path(VECTORSTORE_FOLDER).mkdir(exist_ok=True)

    texts = [doc["text"] for doc in documents]

    if not texts:
        return

    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(documents, f)


def search_documents(query: str, top_k: int = 5):
    if not Path(INDEX_PATH).exists() or not Path(METADATA_PATH).exists():
        return []

    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "rb") as file:
        documents = pickle.load(file)

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype="float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for distance, index_position in zip(distances[0], indices[0]):
        if index_position == -1:
            continue

        if distance > 1.2:
            continue

        document = documents[index_position]

        results.append({"filename": document["filename"], "distance": round(float(distance), 3)})

    return results


def build_document_summary(filename: str, doc_class: str, fields: dict) -> str:
    """
    Builds a readable summary for embedding.
    More meaningful than raw text for semantic search.
    """
    if doc_class == "Invoice":
        return (
            f"This is an invoice from company {fields.get('company', '')} "
            f"with invoice number {fields.get('invoice_number', '')} "
            f"dated {fields.get('date', '')} "
            f"with total amount {fields.get('total_amount', '')}."
        )
    elif doc_class == "Resume":
        return (
            f"This is a resume of {fields.get('name', '')} "
            f"with email {fields.get('email', '')} "
            f"and {fields.get('experience_years', '')} years of experience."
        )
    elif doc_class == "Utility Bill":
        return (
            f"This is a utility bill with account number {fields.get('account_number', '')} "
            f"dated {fields.get('date', '')} "
            f"with usage {fields.get('usage_kwh', '')} kWh "
            f"and amount due {fields.get('amount_due', '')}."
        )
    else:
        return f"This is a general document named {filename}."