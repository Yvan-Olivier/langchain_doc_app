"""The goal of this file is to ingest the data from the source and store it in the database."""

import os
from dotenv import load_dotenv

# langchain libraries
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()
embeddings = OllamaEmbeddings(model="llama3.2:latest")

def ingest_data():
    """Ingest the data from the source and store it in the database."""
    
    loader = ReadTheDocsLoader("langchain_doc")
    raw_docs = loader.load()
    print(f"Loaded {len(raw_docs)} documents")

    # Split the documents into sentences
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    split_docs = splitter.split_documents(raw_docs)
    print(f"Split into {len(split_docs)} documents")

    # Update url for each document to point to the current documentation
    for doc in split_docs:
        source = doc.metadata["source"]
        # Transform local path to current documentation URL
        # Example input: langchain_doc/en/latest/modules/chains/index.html
        # Example output: https://python.langchain.com/docs/modules/chains
        
        raw_path = source.split("langchain_doc/")[1]
        clean_path = (
            raw_path
            .replace("en/latest/", "")  # Remove version path
            .replace(".html", "")       # Remove .html extension
            .replace("index", "")       # Remove index
            .rstrip("/")               # Remove trailing slash
        )
        
        new_url = f"https://python.langchain.com/docs/{clean_path}"
        doc.metadata.update({"source": new_url})

    # Create a Pinecone vector store from the document chunks
    PineconeVectorStore.from_documents(
        documents=split_docs,
        embedding=embeddings,
        index_name=os.getenv("PINECONE_INDEX_NAME")
    )
    
    print("Data successfully loaded into Pinecone")

if __name__ == '__main__':
    print("Ingestion started")
    ingest_data()
