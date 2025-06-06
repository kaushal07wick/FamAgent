# 🧠 FamAgent – Research Assistant Agent

**FamAgent** is an intelligent research assistant built using [LangChain](https://www.langchain.com/), [MistralAI](https://mistral.ai), and structured tools. It answers user queries by searching the web, retrieving data from Wikipedia, and saving outputs to a file—all while returning clean, structured JSON.

---

## 🚀 Features

- 🤖 **LLM Agent** powered by `mistral-small-latest`
- 🔍 **Tool usage** including:
  - Web search
  - Wikipedia lookup
  - Save-to-file
- 📄 **Structured Output** using `Pydantic`
- ⚙️ **Extensible architecture** with custom tools
- 🌐 Works in **WSL**, Linux, and other Unix-based systems

---

## 🛠️ Tech Stack

- Python 3.12
- [LangChain](https://python.langchain.com/)
- [MistralAI](https://mistral.ai)
- Pydantic
- dotenv

---

## 🧰 Tools

### ✅ Included Tools

| Tool         | Description                                  |
|--------------|----------------------------------------------|
| `search_tool`| Perform web searches using custom logic      |
| `wiki_tool`  | Retrieve concise summaries from Wikipedia     |
| `save_tool`  | Save structured output to a local file        |

---

## 🏗️ Project Structure

```

FamAgent/
├── main.py               # Main agent execution script
├── tools.py              # Tool definitions
├── .env                  # Environment variables (Git-ignored)
├── .gitignore            # Git exclusions
├── README.md             # Project documentation
└── agents/               # Python virtual environment (ignored)

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

### 4. Configure Environment

Create a `.env` file and add your Mistral or other API keys:

```dotenv
MISTRAL_API_KEY=your_api_key_here
```

### 5. Run the Agent

```bash
python main.py
```

---

## 💡 Example Output

After entering a query, you’ll get structured output like:

```json
{
  "topic": "Computers",
  "summary": "Computers are electronic devices...",
  "sources": ["https://en.wikipedia.org/wiki/Computer"],
  "tools_used": ["wikipedia"]
}
```

---

## 📎 Notes

* Make sure to use a valid model name (e.g., `mistral-small-latest`)
* Tool names **must follow naming rules**: only letters, digits, underscores, and dashes, max 64 characters

---

## 📜 License

This project is licensed under the MIT License.
