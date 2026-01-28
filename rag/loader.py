import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def load_documents(folder):
    docs = []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        lower = file.lower()

        #  Assign category based on filename
        if "fire" in lower:
            doc_type = "fire"
        elif "flood" in lower:
            doc_type = "flood"
        elif "accident" in lower or "injury" in lower:
            doc_type = "accident"
        elif "green" in lower or "corridor" in lower:
            doc_type = "ambulance"
        elif "motor" in lower or "act" in lower:
            doc_type = "law"
        elif "sop" in lower or "disaster" in lower:
            doc_type = "disaster"
        else:
            doc_type = "general"

        #  Load PDF/TXT
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            file_docs = loader.load()

        elif file.endswith(".txt"):
            loader = TextLoader(path)
            file_docs = loader.load()

        else:
            continue

        #  Attach metadata
        for d in file_docs:
            d.metadata["doc_type"] = doc_type
            d.metadata["source"] = file

        docs.extend(file_docs)

    return docs
