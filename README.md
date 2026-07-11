# AI Blog Writing Agent

An intelligent multi-agent blog generation system built with **LangGraph**, **LangChain**, **Ollama**, **Gemini Image API**, and **Streamlit**.

The application automatically determines whether a topic requires external research, gathers supporting evidence, creates a structured writing plan, generates blog sections in parallel, and produces a final Markdown blog with AI-generated technical diagrams.

---

## Features

- Multi-agent workflow using LangGraph
- Automatic research routing
- Web search integration using Tavily
- Parallel blog section generation
- AI-generated technical diagrams
- Markdown export
- Downloadable blog bundle (Markdown + Images)
- Past blog management
- Live workflow progress in Streamlit

---

# Quick Start

## Prerequisites

- Python 3.11+
- Ollama
- Llama 3.1 model
- Google Gemini API Key
- Tavily API Key

---

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI-Blog-Writing-Agent.git

cd AI-Blog-Writing-Agent
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create .env

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

## 5. Install Ollama

Download Ollama from

https://ollama.com/download

Pull the model

```bash
ollama pull llama3.1:latest
```

Run Ollama

```bash
ollama serve
```

---

## 6. Run Application

```bash
streamlit run frontend.py
```

Open

```
http://localhost:8501
```

---

# Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

> **Note**
>
> Ollama is currently expected to run on the host machine.
> Only the Streamlit application is containerized.

---

# Project Structure

```text
AI-Blog-Writing-Agent/
│
├── backend/                     # Complete LangGraph backend
│   ├── app.py                   # Builds and compiles the workflow graph
│   ├── router.py                # Decides whether research is required
│   ├── research.py              # Performs Tavily search and extracts evidence
│   ├── orchestrator.py          # Creates blog plan and distributes tasks
│   ├── worker.py                # Generates individual blog sections
│   ├── reducer.py               # Merges content and generates images
│   ├── llm.py                   # Shared Ollama LLM configuration
│   ├── schemas.py               # Pydantic models
│   ├── state.py                 # LangGraph shared state
│   └── __init__.py              # Makes backend a Python package
│
├── frontend.py                  # Streamlit user interface
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Container configuration
├── requirements.txt             # Python dependencies
└── README.md
```

---

# Workflow

```
                              User Topic
                                   │
                                   ▼
                         ┌─────────────────┐
                         │  Router Agent   │
                         └────────┬────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
                  ▼                               ▼
        Closed Book Mode                 Research Required
                  │                               │
                  │                     Tavily Web Search
                  │                               │
                  │                     Evidence Extraction
                  └───────────────┬───────────────┘
                                  ▼
                        Orchestrator Agent
                                  │
                     Creates Blog Writing Plan
                                  │
                                  ▼
                    Parallel Worker Agents
                                  │
                      Write Individual Sections
                                  ▼
                         Reducer Subgraph
                                  │
                  ┌───────────────┼────────────────┐
                  ▼               ▼                ▼
            Merge Sections   Plan Images   Generate Images
                  │               │                │
                  └───────────────┴────────────────┘
                                  ▼
                       Final Markdown Blog
```

---

# Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Workflow | LangGraph |
| LLM Framework | LangChain |
| Local LLM | Ollama |
| Image Generation | Gemini 2.5 Flash Image |
| Search | Tavily |
| Frontend | Streamlit |
| Validation | Pydantic |

---

# Future Improvements

- PDF Export
- Multi-language Support
- Blog Publishing
- Dockerized Ollama
- Multiple LLM Support