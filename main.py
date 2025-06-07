from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache
import re

load_dotenv()

set_llm_cache(InMemoryCache())

from tools import (
    search_tool,
    wiki_tool,
    save_embed_tool,
    hyb_tool,
    auto_rag_tool,
    alpha_vantage_tool,
    financial_chart_tool,
    arxiv_tool,
    save_txt_with_faiss
)

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    chart_markdown: str | None = None

llm = ChatMistralAI(
    model_name="mistral-small-latest",
    temperature=0,
    max_retries=2,
)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
        "system",
        """
        You are a research assistant that answers queries using tools and returns a final structured JSON result.

        You MUST respond only once all necessary tools are used and a final answer is ready.

        Wrap the final output ONLY using this format:\n{format_instructions}

        DO NOT return tool calls in your final answer. Use tools if necessary, but ensure the final result matches the schema.
        """,
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())



tools = [
    search_tool,
    wiki_tool,
    save_embed_tool,
    arxiv_tool,
    hyb_tool,
    auto_rag_tool,
    alpha_vantage_tool,
    financial_chart_tool
]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

query = input("What do you want to research on?")
raw_response = agent_executor.invoke({"query": query})

# Extract output text
output_str = raw_response.get("output", "")

# Try to extract JSON from the output text
match = re.search(r'\{.*\}', output_str, re.DOTALL)
if match:
    json_str = match.group(0)
    try:
        structured_response = parser.parse(json_str)
        print(structured_response)
        # Embed the summary text into FAISS
        embed_text = f"Topic: {structured_response.topic}\n\nSummary:\n{structured_response.summary}\n\nSources: {', '.join(structured_response.sources)}\nTools Used: {', '.join(structured_response.tools_used)}"
        save_txt_with_faiss(embed_text)

    except Exception as e:
        print("❌ Parsing still failed:", e)
        print("🔎 Raw output:\n", output_str)
else:
    print("❌ No JSON found in model output.")
    print("🔎 Raw output:\n", output_str)
