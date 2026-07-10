from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path
from typing import List, Optional

from google import genai
from google.genai import types

from .schemas import EvidenceItem


# ============================================================
# Tavily Search
# ============================================================

def tavily_search(query: str, max_results: int = 5) -> List[dict]:
    """
    Perform a Tavily web search.
    Returns an empty list if the API key is missing or the request fails.
    """

    if not os.getenv("TAVILY_API_KEY"):
        return []

    try:
        from langchain_community.tools.tavily_search import TavilySearchResults

        tool = TavilySearchResults(max_results=max_results)
        results = tool.invoke({"query": query})

        output = []

        for result in results or []:
            output.append(
                {
                    "title": result.get("title") or "",
                    "url": result.get("url") or "",
                    "snippet": result.get("content") or result.get("snippet") or "",
                    "published_at": result.get("published_date") or result.get("published_at"),
                    "source": result.get("source"),
                }
            )

        return output

    except Exception:
        return []


# ============================================================
# Date Utilities
# ============================================================

def iso_to_date(date_string: Optional[str]) -> Optional[date]:
    """
    Convert an ISO date string to a Python date object.
    """

    if not date_string:
        return None

    try:
        return date.fromisoformat(date_string[:10])
    except Exception:
        return None


# ============================================================
# File Utilities
# ============================================================

def safe_slug(title: str) -> str:
    """
    Convert a title into a filesystem-safe filename.
    """

    slug = title.strip().lower()
    slug = re.sub(r"[^a-z0-9 _-]+", "", slug)
    slug = re.sub(r"\s+", "_", slug).strip("_")

    return slug or "blog"


# ============================================================
# Gemini Image Generation
# ============================================================

def generate_image_bytes(prompt: str) -> bytes:
    """
    Generate an image using Gemini Flash Image.
    Returns raw image bytes.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_ONLY_HIGH",
                )
            ],
        ),
    )

    parts = getattr(response, "parts", None)

    if not parts and getattr(response, "candidates", None):
        try:
            parts = response.candidates[0].content.parts
        except Exception:
            parts = None

    if not parts:
        raise RuntimeError("No image content returned.")

    for part in parts:
        inline = getattr(part, "inline_data", None)

        if inline and getattr(inline, "data", None):
            return inline.data

    raise RuntimeError("No inline image bytes found.")


# ============================================================
# Markdown Writer
# ============================================================

def save_markdown(filename: str, content: str):
    """
    Save markdown content to disk.
    """

    Path(filename).write_text(content, encoding="utf-8")


# ============================================================
# Image Directory
# ============================================================

def ensure_images_directory() -> Path:
    """
    Create the images directory if it doesn't already exist.
    """

    image_dir = Path("images")
    image_dir.mkdir(exist_ok=True)

    return image_dir