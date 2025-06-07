from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import init_chat_model
import os

embedding_model = CohereEmbeddings(
    model="embed-english-v2.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

FAISS_DB_PATH = "research_faiss_index"

model = init_chat_model("command-r-plus", model_provider="cohere", temperature=0)


# Globals to hold FAISS DB and retrieval chain, initialized only when needed
faiss_db = None
retrieval_qa_chain = None

def save_documents_and_create_index(documents: list):
    """
    Embed and save documents into FAISS DB,
    then create retrieval QA chain.
    """
    global faiss_db, retrieval_qa_chain
    if not documents:
        raise ValueError("No documents provided to save.")
    
    # Create FAISS index from documents
    faiss_db = FAISS.from_documents(documents, embedding_model)
    faiss_db.save_local(FAISS_DB_PATH)
    
    retriever = faiss_db.as_retriever()
    retrieval_qa_chain = RetrievalQA.from_chain_type(
    llm=model,
    retriever=retriever,
    return_source_documents=True
)


def load_faiss_if_exists():
    """
    Loads the FAISS DB and retrieval chain if saved on disk.
    """
    global faiss_db, retrieval_qa_chain
    if os.path.exists(FAISS_DB_PATH):
        faiss_db = FAISS.load_local(FAISS_DB_PATH, embedding_model, allow_dangerous_deserialization=True )
        retriever = faiss_db.as_retriever()
        retrieval_qa_chain = RetrievalQA.from_chain_type(
            llm=model,
            retriever=retriever,
            return_source_documents=True
        )
        return True
    return False

def is_faiss_db_populated() -> bool:
    """
    Checks if FAISS DB is loaded and contains vectors.
    """
    if faiss_db is None:
        return False
    try:
        return faiss_db.index.ntotal > 0
    except AttributeError:
        return False

def query_saved_notes(query: str):
    """
    Query the FAISS DB only if loaded and populated.
    """
    if retrieval_qa_chain is None or not is_faiss_db_populated():
        return "No saved notes available yet. Please save embeddings before querying."
    
    return retrieval_qa_chain.run(query)
