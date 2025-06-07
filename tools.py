from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from langchain_hyperbrowser import HyperbrowserBrowserUseTool
from langchain.schema import Document
from alphavan_tool import get_financial_data, generate_financial_chart
from rag_utils import faiss_db, FAISS_DB_PATH, load_faiss_if_exists, save_documents_and_create_index, query_saved_notes
from langchain.schema import Document
from datetime import datetime
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun


def save_txt_with_faiss(data: str, filename: str = "research_output.txt"):
    global faiss_db  # ensure you modify the global faiss_db

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"---Research Output---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    doc = Document(page_content=data, metadata={"timestamp": timestamp})

    if load_faiss_if_exists():
        faiss_db.add_documents([doc])
        faiss_db.save_local(FAISS_DB_PATH)
    else:
        save_documents_and_create_index([doc])

    return f"Data saved to {filename} and embedded in FAISS index."


save_embed_tool = Tool(
    name="Save_and_Embed_to_FAISS",
    func=save_txt_with_faiss,
    description="Save research notes in a text file and store them as vector embeddings for later use"
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search_Web",
    func=search.run,
    description="Search the web for any information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

hyb_tool = HyperbrowserBrowserUseTool()

# Define the RAG tool
auto_rag_tool = Tool(
    name="Ask_Saved_Research",
    func=query_saved_notes,
    description="Ask a question using saved research notes with retrieval-augmented generation"  # You can insert your description here
)

alpha_vantage_tool = Tool(
    name="Alpha_Vantage_Financial_Data",
    func=get_financial_data,
    description="Query financial data such as stock prices, currency exchange rates, and market sentiment using Alpha Vantage. Example queries: 'Get exchange rate USD to INR', 'Get daily stock for IBM', 'Get market news for AAPL'."
)


financial_chart_tool = Tool(
    name="Financial_Chart_Generator",
    func=generate_financial_chart,
    description="Generates daily price or volume charts using Alpha Vantage data. Try: 'daily chart for AAPL' or 'volume chart for IBM'."
)


# Initialize arxiv query run tool
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())

# Wrap the arxiv tool as a langchain Tool with a callable func
arxiv_tool = Tool(
    name="ArxivSearch",
    func=arxiv.run,  # pass the run method, which takes a query string
    description="Search scientific papers on Arxiv and return publication details"
)