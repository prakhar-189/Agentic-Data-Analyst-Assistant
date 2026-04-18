# 🤖 Agentic EDA Engine

**A self-correcting, LLM-powered Exploratory Data Analysis agent that writes, executes, and debugs its own Python code — so you don't have to.**

---

## Overview

Agentic EDA Engine is an AI-driven data analysis assistant that lets you explore datasets using plain English. Instead of writing pandas or matplotlib code yourself, you simply upload a file, ask a question, and the agent takes care of the rest — autonomously generating, running, and fixing code until it gets the right answer.

Under the hood, the system is built as a **stateful agentic workflow** using [LangGraph](https://github.com/langchain-ai/langgraph), with a local LLM ([Qwen2.5-Coder:7b](https://ollama.com/library/qwen2.5-coder) via Ollama) for code generation. A [Streamlit](https://streamlit.io/) front-end provides a clean, chat-based interface for interacting with your data.

---

## How It Works

The agent follows a **Generate → Execute → Reflect** loop:

1. **Generate**: The LLM receives your natural language query and the dataset's schema (columns, data types, sample rows) and generates Python analysis code.
2. **Execute**: The generated code is run in a sandboxed environment. If it succeeds, the output (text results or charts) is returned to you.
3. **Reflect**: If the code throws an error, the agent analyzes the error message and rewrites the code to fix it. This loop continues for up to 3 iterations before gracefully stopping to prevent infinite loops.
4. **Clarify**: If your query is ambiguous, the agent pauses and asks you for clarification instead of guessing.

This self-correcting loop means the agent can recover from common mistakes — wrong column names, incorrect data types, missing imports — without any intervention from you.

---

## Features

- 🗣️ **Natural language querying** — ask questions like *"What is the average revenue by region?"* or *"Plot monthly sales trends"*
- 🔁 **Self-correcting execution** — automatically rewrites and retries code on failure (up to 3 times)
- 📊 **Chart generation** — produces and displays matplotlib/seaborn plots directly in the UI
- 🗂️ **Schema-aware generation** — uses extracted column names, data types, and sample rows to write accurate, context-aware code
- 📁 **CSV & Excel support** — works with both `.csv` and `.xlsx` file formats
- 🔒 **Fully local** — runs entirely on your machine via Ollama; no data is sent to external APIs
- 🧾 **Transparent outputs** — view the final executed code and the number of correction iterations in an expandable panel

---

## Project Structure

```
Agentic-EDA-Engine/
│
├── main.py              # Core agentic workflow (LangGraph state graph)
├── streamlit_app.py     # Streamlit UI — file upload, chat interface, result display
├── prompts.py           # Prompt templates for code generation and error reflection
├── tools.py             # Safe Python code execution utility
├── requirements.txt     # Python dependencies
├── Sample Datasets/     # Example datasets to try out
├── output/              # Temporary folder for generated chart images
└── sample_generated.ipynb  # Example notebook showing generated outputs
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Agentic Workflow | LangGraph |
| LLM | Qwen2.5-Coder:7b via Ollama (local) |
| LLM Interface | LangChain Ollama |
| UI | Streamlit |
| Data Handling | Pandas |
| Visualization | Matplotlib / Seaborn |

---

## Getting Started

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running locally
- Qwen2.5-Coder model pulled: `ollama pull qwen2.5-coder:7b`

### Installation

```bash
git clone https://github.com/PrakharSri18-data/Agentic-EDA-Engine.git
cd Agentic-EDA-Engine
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run streamlit_app.py
```

Then open `http://localhost:8501` in your browser.

---

## Usage

1. Launch the Streamlit app.
2. Upload a `.csv` or `.xlsx` dataset using the file uploader.
3. Review the automatically extracted schema in the expandable panel.
4. Type your analysis question in the chat input (e.g., *"Show me the top 5 products by total sales"*).
5. The agent will generate, execute, and if necessary, self-correct Python code to answer your question.
6. View the result, any generated charts, the final code, and the number of correction loops it took.

---

## Example Queries

- `"What is the distribution of customer ages?"` → Generates a histogram
- `"Which city had the highest total revenue last year?"` → Returns a ranked summary
- `"Plot the correlation between price and quantity sold"` → Generates a scatter plot
- `"Are there any missing values in the dataset?"` → Returns a missing-value report

---

## Limitations

- The agent uses a local LLM, so performance depends on your hardware (GPU recommended for Qwen2.5-Coder:7b).
- Complex, multi-step analyses may occasionally require rephrasing the query for best results.
- The maximum self-correction attempts are capped at 3 iterations to prevent runaway loops.

---

## License

This project is licensed under the [MIT License](LICENSE) © Prakhar Srivastava

---

## Acknowledgements

Built with [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), [Ollama](https://ollama.com/), and [Streamlit](https://streamlit.io/).

---

## Author

Prakhar Srivastava

Data Analyst, Data Scientist & AI Engineer | Dashboards, SQL, Machine Learning, Deep Learning, Generative AI, Prompt Engineering & Agentic AI
