from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.chat_models import init_chat_model
from datetime import datetime
import os

# Global FAISS setup
FAISS_DB_PATH = "research_faiss_index"
faiss_db = None
retrieval_qa_chain = None

# cohere-embedding model                 # can change it to any other model
embedding_model = CohereEmbeddings(
    model="embed-english-v2.0",
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    user_agent="famagent/1.0"  # Add a user_agent string here
)


# model initialization
model = init_chat_model("command-r-plus", model_provider="cohere", temperature=0)

# saving the data and indexig to FAISS database
def save_to_faiss(data: str):
    """
    Embed text into FAISS vector store.
    """
    global faiss_db, retrieval_qa_chain

    doc = Document(page_content=data, metadata={"timestamp": datetime.now().isoformat()})

    if os.path.exists(FAISS_DB_PATH):
        faiss_db = FAISS.load_local(FAISS_DB_PATH, embedding_model, allow_dangerous_deserialization=True)
        faiss_db.add_documents([doc])
    else:
        faiss_db = FAISS.from_documents([doc], embedding_model)

    faiss_db.save_local(FAISS_DB_PATH)

    retriever = faiss_db.as_retriever()
    retrieval_qa_chain = RetrievalQA.from_chain_type(llm=model, retriever=retriever, return_source_documents=True)

    return "✅ Data embedded into FAISS."

# Auto-RAG functionality
def query_notes(query: str):
    """
    Query notes from FAISS if available.
    """
    if retrieval_qa_chain is None or faiss_db is None or getattr(faiss_db.index, "ntotal", 0) == 0:
        return "No saved notes yet. Please save data first."

    return retrieval_qa_chain.run(query)