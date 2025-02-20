import os
from dotenv import load_dotenv

# Langchain libraries
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain import hub

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


load_dotenv()

def run_llm(query: str):
    """Run the LLM model to generate a response to the query."""
    
    print("Retrievving...")

    llm = ChatOllama(model="llama3.2:latest")
    embeddings = OllamaEmbeddings(model="llama3.2:latest")

    # Create a Pinecone vector store from the document chunks
    vectorstore = PineconeVectorStore(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        embedding=embeddings,
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    # Create a stuff documents chain
    combine_docs_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=retrieval_qa_chat_prompt,
    )

    # Create a retrieval chain  
    retrieval_qa_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=combine_docs_chain,
    )
    
    # Run the chain
    result = retrieval_qa_chain.invoke({"input": query})
    
    return {
        "answer": result["answer"],
        "sources": [doc.metadata for doc in result["context"]]
    }

if __name__ == '__main__':
    query = "What is a langchain chain?"
    response = run_llm(query)
    print(response)




