"""
RAG (Retrieval-Augmented Generation) System

This is the "knowledge library" for WealthMind.
We store investment wisdom as text chunks in a vector database (ChromaDB).
When answering a question, we first RETRIEVE relevant knowledge,
then AUGMENT the LLM prompt with it.

Flow:
  User query → embed → similarity search → top chunks → add to LLM prompt
"""

import os
from dotenv import load_dotenv

from typing import List
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
# Where ChromaDB saves its data on disk
CHROMA_PATH = os.getenv("CHROMA_PATH")


def get_vector_store() -> Chroma:
    """
    Returns the ChromaDB vector store.
    Creates it if it doesn't exist yet.
    """
    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    
    store = Chroma(
        collection_name="investment_knowledge",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH,
    )
    return store


def retrieve_relevant_knowledge(query: str, k: int = 3) -> str:
    """
    Finds the top-k most relevant knowledge chunks for a given query.
    
    Args:
        query: what we're looking for (e.g. "strategies for retirement")
        k: how many results to return
    
    Returns:
        A single string with all relevant knowledge joined together.
        This gets injected into our LLM prompt.
    """
    store = get_vector_store()
    
    # Similarity search: finds chunks closest to our query
    docs = store.similarity_search(query, k=k)
    
    if not docs:
        return "No specific knowledge found. Using general investment principles."
    
    # Join all retrieved chunks
    knowledge = "\n\n---\n\n".join([doc.page_content for doc in docs])
    return knowledge


def add_documents(texts: List[str]) -> None:
    """
    Adds new knowledge to the vector store.
    Used by ingest.py to populate the database.
    """
    store = get_vector_store()
    
    # Split long texts into smaller chunks for better retrieval
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # max 500 characters per chunk
        chunk_overlap=50,      # 50 char overlap to keep context
    )
    
    all_chunks = []
    for text in texts:
        chunks = splitter.split_text(text)
        all_chunks.extend(chunks)
    
    store.add_texts(all_chunks)
    print(f"[INFO] Added {len(all_chunks)} knowledge chunks to vector store")



