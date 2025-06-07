import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache
from typing import List
from langchain_ollama.chat_models import ChatOllama

# Load environment and initialize cache
load_dotenv()
set_llm_cache(InMemoryCache())

# Import tools
from famagent.tools import (
    search_tool,
    wiki_tool,
    save_text_tool,
    save_faiss_tool,
    auto_rag_tool,
    arxiv_tool,
)

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]

# Initialize LLM
llm = ChatMistralAI(
    model_name="mistral-small-latest",
    temperature=0,
    max_retries=2,
)

# Output parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Improved prompt with better structure and explicit JSON formatting
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert research assistant with tool-using capabilities. 
            Your task is to understand the user's query, break it into actionable steps, and execute them sequentially using appropriate tools.
            {format_instructions}""",
                    ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Tools list
tools = [
    search_tool,
    wiki_tool,
    save_text_tool,
    save_faiss_tool,
    arxiv_tool,
    auto_rag_tool,
]

# Agent and executor
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)


def run_query(query: str):
    response = agent_executor.invoke({"query": query})
        

def display_research_from_tool_calls(tool_calls: list):
    """Display formatted research content extracted from tool call output."""
    if not tool_calls:
        st.warning("No tool call data found.")
        return

    for idx, item in enumerate(tool_calls, 1):
        name = item.get("name", "")
        arguments = item.get("arguments", {})

        if name == "Save_Text_File":
            content = arguments.get("__arg1", "").strip()

            if content:
                st.markdown(f"## 📄 Research Output #{idx}")
                st.markdown("### 📝 Summary")
                st.write(content)
                st.success("✅ Successfully extracted content from Save_Text_File")
            else:
                st.warning(f"No content found in Save_Text_File #{idx}.")
        else:
            st.info(f"Ignoring tool call: {name}")


def main():
    st.set_page_config(
        page_title="FamAgent Research Tool",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 FamAgent: AI Agent for General Research")
    st.markdown("*Powered by Mistral AI with advanced tool integration*")
    
    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        query = st.text_area(
            "Enter your research query:",
            height=100,
            placeholder="e.g., 'Research the latest developments in quantum computing and save the findings'"
        )
    
    with col2:
        st.markdown("### 🛠️ Available Tools")
        st.markdown("""
        - 🔍 **Search Tool**: Web search
        - 📖 **Wiki Tool**: Wikipedia lookup
        - 💾 **Save Text**: Save to file
        - 🗃️ **FAISS Tool**: Vector embedding
        - 📚 **ArXiv Tool**: Academic papers
        - 🧠 **Auto RAG**: Memory search
        """)
    
    if st.button("🚀 Run Research", type="primary") and query:
        with st.spinner("🔬 Conducting research..."):
            result = run_query(query)
        
        print("the actual f out")
        print(result)
        
        # Display results
        display_research_from_tool_calls(result)

        st.text(result)
        


# Run the app
if __name__ == "__main__":
    main()