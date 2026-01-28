from langchain_community.vectorstores import Chroma
import chromadb


def build_vector_db(chunks, embedder):
    """
    Safely rebuild Chroma DB on Windows 
    Clears old collection properly without file deletion
    """

    persist_dir = "db/chroma"
    collection_name = "emergency_protocols"

    #  Create Chroma client
    client = chromadb.PersistentClient(path=persist_dir)

    #  Delete old collection if exists
    try:
        client.delete_collection(collection_name)
        print("🗑 Old collection deleted successfully.")
    except:
        pass  # Collection may not exist first time

    #  Create new clean collection
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        collection_name=collection_name,
        persist_directory=persist_dir
    )

    return vector_db


def load_existing_db(embedder):
    return Chroma(
        persist_directory="db/chroma",
        embedding_function=embedder,
        collection_name="emergency_protocols"
    )
