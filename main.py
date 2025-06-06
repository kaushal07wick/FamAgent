from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
import re
import json
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

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
        You are a research assistant that will help generate a research paper.
        Answer the user query and use necessary tools.
        Wrap the output in this format and provide no other text:\n{format_instructions}
        """,
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]

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
    except Exception as e:
        print("❌ Parsing still failed:", e)
        print("🔎 Raw output:\n", output_str)
else:
    print("❌ No JSON found in model output.")
    print("🔎 Raw output:\n", output_str)
