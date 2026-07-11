# ChatOllama initialization

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv()

# Shared LLM instance
llm = ChatOllama(
    model="llama3.1:latest",
    temperature=0.2,
    max_output_tokens=2026,
)