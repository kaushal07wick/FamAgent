from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from utils import save_txt_only
from famagent.rag import save_to_faiss, query_notes
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun

# Save to Text File Tool
save_text_tool = Tool(
    name="Save_Text_File",
    func=save_txt_only,
    description="Save research notes in a timestamped text file"
)

# FAISS VectorStore Tool
save_faiss_tool = Tool(
    name="Embed_to_FAISS",
    func=save_to_faiss,
    description="Embed research notes into the FAISS vector store for semantic retrieval"
)

# DuckDuckGo Web Search Tool
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search_Web",
    func=search.run,
    description="Search the web for any information",
)

# Wikipedia Tool
api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


# auto-RAG Tool
auto_rag_tool = Tool(
    name="Ask_Saved_Research",
    func=query_notes,
    description="Ask a question using saved research notes with retrieval-augmented generation"  # You can insert your description here
)

# Arxiv Tool
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())
arxiv_tool = Tool(
    name="ArxivSearch",
    func=arxiv.run,  
    description="Search scientific papers on Arxiv and return publication details"
)