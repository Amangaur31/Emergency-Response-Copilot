from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embedder import get_embedder
from rag.retriever import retrieve_top_chunks
from rag.llm import get_llm
from rag.vector_db import build_vector_db, load_existing_db
import os
import shutil


class RAGPipeline:
    def __init__(self):
        self.embedder = get_embedder()
        self.llm = get_llm()
        #  Auto-load existing DB if available
        if os.path.exists("db/chroma"):
            print(" Loading existing emergency protocol DB...")
            self.vector_db = load_existing_db(self.embedder)
        else:
            self.vector_db = None

    # -------------------------------
    # Step 1: Index Documents
    # -------------------------------
    def index_folder(self, folder: str):

        print("Loading documents...")
        docs = load_documents(folder)

        if not docs:
            raise ValueError(
                " No documents found. Add at least one PDF/TXT inside books/ folder."
            )

        print("Splitting into chunks...")
        chunks = split_documents(docs)

        if not chunks:
            raise ValueError(" No chunks created. Document may be empty.")

        print("Building Vector DB (Safe Re-index)...")

        #  Just rebuild collection safely (no folder delete)
        self.vector_db = build_vector_db(chunks, self.embedder)

        print(f" Indexed {len(chunks)} chunks successfully.")



    # -------------------------------
    # Step 2: Ask Question
    # -------------------------------
    def ask(self, question: str, emergency_type="general"):
        if not self.vector_db:
            return " Please index documents first.", []

        #  Retrieve top chunks
        docs = retrieve_top_chunks(question, self.vector_db, k=10, emergency_type=emergency_type)

        #  Build context
        context = "\n\n".join([d.page_content for d in docs])

        #  Emergency Response Copilot Prompt
        prompt = f"""
You are **EmergencyLane AI**, a Smart Traffic + Emergency Response Copilot.

Your job is to assist:
- Ambulance drivers
- Traffic police officers
- Smart City control rooms

You will be given official emergency and traffic protocol context.

 RULES:
- Answer ONLY from the context provided.
- Do NOT copy-paste full sentences.
- Rewrite clearly in simple, actionable language.
- Provide step-by-step emergency guidance.
- If protocol is missing, say: "Not found in emergency documents."

-------------------------
OFFICIAL PROTOCOL CONTEXT:
{context}
-------------------------

LIVE EMERGENCY QUERY:
{question}

Respond strictly in this format:

 Situation Summary:
(1–2 lines)

 Immediate Actions:
- Step 1
- Step 2
- Step 3

 Traffic Management Guidance:
- What police/public should do

 Safety Note:
(Important caution if applicable)

 Protocol Reference:
(Mention that answer is based on provided documents)

Final Answer:
"""

        #  LLM Response
        response = self.llm.invoke(prompt)

        #  Sources
        sources = []
        for d in docs:
            page = d.metadata.get("page", "?")
            source = d.metadata.get("source", "document")
            sources.append(f"{source} (page {page})")

        sources = sorted(set(sources))

        #  Extract clean answer
        answer_text = response.content

        if isinstance(answer_text, list):
            cleaned_parts = []
            for part in answer_text:
                if isinstance(part, dict) and "text" in part:
                    cleaned_parts.append(part["text"])
                else:
                    cleaned_parts.append(str(part))
            answer_text = " ".join(cleaned_parts)

        elif isinstance(answer_text, dict) and "text" in answer_text:
            answer_text = answer_text["text"]

        answer_text = str(answer_text).strip()

        return answer_text, sources
