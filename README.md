# 🧠 FamAgent – Research Assistant Agent

**FamAgent** (**F**unctional **A**ssistant for **M**eaningful Research **Agent**) is an intelligent research assistant built using [LangChain](https://www.langchain.com/), and Models from **Ollama**, **FAISS** with **Streamlit** as frontend and a powerful suite of structured tools.

It helps you by:

- Searching the web for the latest information  
- Retrieving concise summaries from Wikipedia  
- Fetching academic papers from sources like arXiv  
- Saving outputs efficiently for further use  

All responses are delivered as clean, structured JSON, making integration and analysis seamless.

---

## 🚀 Features

- 🤖 **LLM Agent** powered by Langchain models (here : `mistral`) or any model can be served locally via **Ollama**
- 🔍 **Multi-tool integration** including:
  - Web search & Wikipedia lookup
  - Academic paper retrieval from arXiv
  - Automated Retrieval-Augmented Generation (Auto-RAG)
  - Saving and embedding outputs for later search
- 📄 **Structured Output** with `Pydantic` schemas
- ⚙️ **Extensible architecture** supporting custom tools
---

## 🧰 Tools

### ✅ Included Tools & Usage

| Tool Name        | Description                                                                                   | Example Commands                               |
|------------------|-----------------------------------------------------------------------------------------------|------------------------------------------------|
| `search_tool`    | Perform broad web searches to gather up-to-date information                                   | "Search for latest AI breakthroughs"           |
| `wiki_tool`      | Retrieve concise, reliable summaries from Wikipedia                                           | "Explain quantum computing from Wikipedia"     |
| `save_embed_tool`| Save research notes as text files and embed them into a FAISS vector store for semantic search| (Automatically used internally when saving)    |
| `arxiv_tool`     | Search and retrieve academic papers from arXiv                                                | "Find recent papers on reinforcement learning" |
| `auto_rag_tool`  | Automatic Retrieval-Augmented Generation: combines retrieval and generation for in-depth answers| "Summarize recent advances in renewable energy"|

---

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/famagent.git
cd famagent
````

### 2. Install Using `install.sh`

Run the installation script to setup your environment and dependencies:

```bash
./install.sh
```

### OR: Install Editable Package with pip

```bash
python3 -m venv agents
source agents/bin/activate  # or `source agents/Scripts/activate` on Windows
pip install -e .
```

### 3. Configure Environment Variables

Create a `.env` file and add your API keys:

```dotenv
MISTRAL_API_KEY=your_api_key_here
COHERE_API_KEY=your_cohere_api_key
```

---

## 🛠️ Using Ollama for Local Model Serving

This project uses [Ollama](https://ollama.com/) to serve the Mistral model locally for fast and private inference.

### Steps to Setup Ollama

1. **Install Ollama**

Follow instructions at [Ollama Install Docs](https://ollama.com/docs/install)

2. **Download and Run the Mistral Model**

```bash
ollama pull mistral/mistral-small
```

3. **Run Ollama Server**

Make sure the Ollama daemon is running locally.

4. **Configure your `.env`**

Set the model provider in your `.env`:

```dotenv
MODEL_PROVIDER=ollama
OLLAMA_MODEL_NAME=mistral/mistral-small
```

The code will connect to the Ollama model endpoint automatically.

---

## 💡 Running the Agent

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser to access the Streamlit UI.

---

## 💡 Example Output

Upon entering your query, you receive a structured JSON response like this:

```json
{
  "topic": "Artificial Intelligence",
  "summary": "Artificial Intelligence (AI) refers to ...",
  "sources": ["https://en.wikipedia.org/wiki/Artificial_intelligence"],
  "tools_used": ["search_tool", "wiki_tool"],
}
```

---

## 📜 License

This project is licensed under the MIT License.
