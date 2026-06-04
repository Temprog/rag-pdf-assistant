import streamlit as st
from dotenv import load_dotenv
import os
import numpy as np
import json
from datetime import datetime

load_dotenv()

st.title("AI Banking Regulations Assistant (RAG System)")

# =========================================================
# # CONFIG
# If USE_OPENAI = False → uses HuggingFace embeddings (free, local)
# If USE_OPENAI = True  → uses OpenAI embeddings and/or LLM (paid API)
# =========================================================
USE_OPENAI = False  # Toggle between OpenAI (cloud LLM/embeddings, paid API) and HuggingFace (local embeddings, free)
PERSIST_DIR = "chroma_db"

# =========================================================
# LOAD DOCUMENT
# =========================================================
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("documents/fca_operational_resilience.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

# =========================================================
# EMBEDDINGS (LOCAL OR OPENAI)
# =========================================================
if USE_OPENAI:
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings()
else:
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

# =========================================================
# VECTOR DB (CACHED)
# =========================================================
from langchain_community.vectorstores import Chroma

if os.path.exists(PERSIST_DIR):
    db = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )
else:
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=PERSIST_DIR
    )
    db.persist()

retriever = db.as_retriever()

# =========================================================
# LLM
# =========================================================
if USE_OPENAI:
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
else:
    llm = None

# =========================================================
# SAFETY / GUARDRAILS
# =========================================================
def is_safe_query(query):
    banned_keywords = [
        "hack", "exploit", "fraud", "bypass", "illegal"
    ]
    return not any(word in query.lower() for word in banned_keywords)

# =========================================================
# LOGGING (AUDIT TRAIL - BANKING STYLE)
# =========================================================
def log_interaction(question, answer, score):
    log_entry = {
        "timestamp": str(datetime.now()),
        "question": question,
        "answer": answer,
        "score": score
    }

    with open("audit_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# =========================================================
# USER INPUT
# =========================================================
question = st.text_input("Ask a question about FCA regulations")

if question:

    # -------------------------
    # Guardrail check
    # -------------------------
    if not is_safe_query(question):
        st.error("Query blocked due to safety policy.")
        st.stop()

    # -------------------------
    # RETRIEVAL
    # -------------------------
    docs = retriever.invoke(question)

    context = "\n\n".join([d.page_content for d in docs])

    # -------------------------
    # EVALUATION SCORE
    # -------------------------
    q_vec = embeddings.embed_query(question)

    scores = []
    for d in docs:
        d_vec = embeddings.embed_query(d.page_content)

        score = np.dot(q_vec, d_vec) / (
            np.linalg.norm(q_vec) * np.linalg.norm(d_vec)
        )

        scores.append(score)

    avg_score = float(np.mean(scores))

    # -------------------------
    # LLM GENERATION
    # -------------------------
    answer_text = None

    if llm:
        prompt = f"""
You are a banking compliance assistant.

Only answer using the provided context.

If context is insufficient, say "Not enough information in the document."

Context:
{context}

Question:
{question}
"""

        result = llm.invoke(prompt)
        answer_text = result.content

    # -------------------------
    # UI OUTPUT
    # -------------------------
    st.subheader("Answer")
    st.write(answer_text if answer_text else "LLM disabled")

    st.subheader("Evaluation Score")
    st.metric("Context Match", f"{avg_score:.2f}")

    # -------------------------
    # CITATIONS
    # -------------------------
    st.subheader("Citations (Page References)")

    for d in docs:
        page = d.metadata.get("page", None)
        st.write(f"📄 Page {page + 1 if page else 'Unknown'}")
        st.write(d.page_content[:250])
        st.write("---")

    # -------------------------
    # AUDIT LOGGING
    # -------------------------
    log_interaction(question, answer_text, avg_score)