from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

# ============================================================
# LLM Configuration
# ============================================================

OLLAMA_MODEL = "llama3.1:latest"

TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 2026

llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=TEMPERATURE,
    max_output_tokens=MAX_OUTPUT_TOKENS,
)