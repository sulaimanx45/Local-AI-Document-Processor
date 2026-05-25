from pypdf import PdfReader
import glob
import os

"""LOADING DOCUMENTS"""
def read_all_documents(folder_path="data"):
   
    documents = {}

    pdf_files = glob.glob(f"{folder_path}/*.pdf")
    txt_files = glob.glob(f"{folder_path}/*.txt")
    all_files = pdf_files + txt_files

    if not all_files:
        return documents

    for file in all_files:
        filename = os.path.basename(file)

        if file.endswith(".pdf"):
            reader = PdfReader(file)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += " " + text.replace("\n", " ")

        elif file.endswith(".txt"):
            with open(file, "r", encoding="utf-8") as f:
                full_text = f.read()
        documents[filename] = " ".join(full_text.split())

    return documents
