# 🧠 FamAgent – Research Assistant Agent

**FamAgent** is an intelligent research assistant built using [LangChain](https://www.langchain.com/), [MistralAI](https://mistral.ai), and a suite of structured tools. It answers your queries by searching the web, retrieving Wikipedia summaries, accessing financial data, fetching academic papers, generating charts, and saving outputs—all while returning clean, structured JSON.

---

## 🚀 Features

- 🤖 **LLM Agent** powered by `mistral-small-latest`
- 🔍 **Multi-tool integration** including:
  - Web search & Wikipedia lookup
  - Academic paper retrieval from arXiv
  - Financial data and chart generation
  - Automated Retrieval-Augmented Generation (Auto-RAG)
  - Saving and embedding outputs for later search
- 📄 **Structured Output** with `Pydantic` schemas
- ⚙️ **Extensible architecture** supporting custom tools
- 🌐 Compatible with **WSL**, Linux, and Unix-based systems

---

## 🛠️ Tech Stack

- Python 3.12  
- [LangChain](https://python.langchain.com/)  
- [MistralAI](https://mistral.ai)  
- Pydantic  
- dotenv  

---

## 🧰 Tools

### ✅ Included Tools & Usage

| Tool Name             | Description                                                                                       | Example Commands                                         |
|-----------------------|-------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| `search_tool`          | Perform broad web searches to gather up-to-date information                                     | "Search for latest AI breakthroughs"                     |
| `wiki_tool`            | Retrieve concise, reliable summaries from Wikipedia                                             | "Explain quantum computing from Wikipedia"               |
| `save_embed_tool`      | Save research notes as text files and embed them into a FAISS vector store for semantic search  | (Automatically used internally when saving results)      |
| `arxiv_tool`           | Search and retrieve academic papers from arXiv                                                  | "Find recent papers on reinforcement learning"           |
| `hyb_tool`             | Hyperbrowser is a platform for running, running browser agents, and scaling headless browsers. It lets you launch and manage browser sessions at scale and provides easy to use solutions for any webscraping needs, such as scraping a single page or crawling an entire site.                     | "Look up blockchain technologies"                        |
| `auto_rag_tool`        | Automatic Retrieval-Augmented Generation: combines retrieval and generation for in-depth answers | "Summarize recent advances in renewable energy"          |
| `alpha_vantage_tool`   | Fetch real-time financial data such as stock quotes, exchange rates, and market news            | "Get stock quote for AAPL", "Exchange rate USD to EUR"   |
| `financial_chart_tool` | Generate and save financial charts (price, volume) as PNG images using PIL                      | "Show daily chart for Tesla", "Volume chart for IBM"     |
| `save_txt_with_faiss`  | Save text data and embed it for semantic search using FAISS (internal use)                      | (Automatically invoked to store summaries for retrieval) |

---

## 🗣️ How to Use FamAgent with Tools

You don’t need to invoke tools manually — just ask your question naturally. FamAgent automatically decides which tools to use based on your query. Here are some example prompts and the tools they trigger:

| User Query                                      | Triggered Tool(s)              |
|------------------------------------------------|-------------------------------|
| "Search for the latest developments in AI"     | `search_tool`                  |
| "Explain black holes from Wikipedia"            | `wiki_tool`                    |
| "Find recent research papers on climate change"| `arxiv_tool`                   |
| "Get the current stock price of Microsoft"     | `alpha_vantage_tool`           |
| "Show me a daily price chart for Apple"         | `financial_chart_tool`         |
| "Summarize recent progress in fusion energy"   | `auto_rag_tool` (retrieval + generation) |
| "Save this summary for future reference"        | `save_embed_tool` (automatic)  |

---

## 🏗️ Project Structure

```

FamAgent/
├── main.py               # Main agent execution script
├── tools.py              # Tool definitions and wrappers
├── .env                  # Environment variables (Git-ignored)
├── .gitignore            # Git exclusions
├── README.md             # Project documentation
└── agents/               # Python virtual environment (ignored)

````

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/famagent.git
cd famagent
````

### 2. Create Virtual Environment

```bash
python3 -m venv agents
source agents/bin/activate  # or `source agents/Scripts/activate` on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and add your API keys:

```dotenv
MISTRAL_API_KEY=your_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

### 5. Run the Agent

```bash
python main.py
```

---

## 💡 Example Output

Upon entering your query, you receive a structured JSON response like this:

```json
{
  "topic": "Artificial Intelligence",
  "summary": "Artificial Intelligence (AI) refers to ...",
  "sources": ["https://en.wikipedia.org/wiki/Artificial_intelligence"],
  "tools_used": ["search_tool", "wiki_tool"],
  "chart_markdown": null
}
```

---

## 📎 Notes

* Ensure you provide valid API keys in `.env`.
* Tool names are alphanumeric with underscores/dashes only, max 64 characters.
* Charts generated by `financial_chart_tool` are saved as PNG files using PIL and can be embedded or saved locally.

---

## 📜 License

This project is licensed under the MIT License.