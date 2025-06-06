from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime


def save_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"---Research Output---\n Timestamp {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"data successfully saved to {filename}"


save_tool = Tool(
    name = "Save_text_to_file",
    func = save_txt,
    description="save the output to a text file0"
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search_Web",
    func=search.run,
    description="Search the web for any information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
