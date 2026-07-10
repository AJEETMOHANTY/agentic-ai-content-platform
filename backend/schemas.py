from __future__ import annotations

import operator
from typing import Annotated, List, Literal, Optional, TypedDict

from pydantic import BaseModel, Field


# ============================================================
# Task & Planning Schemas
# ============================================================

class Task(BaseModel):
    id: int
    title: str
    goal: str = Field(
        ...,
        description="One sentence describing what the reader should do or understand.",
    )

    bullets: List[str] = Field(
        ...,
        min_length=3,
        max_length=6,
    )

    target_words: int = Field(
        ...,
        description="Target number of words for this section.",
    )

    tags: List[str] = Field(default_factory=list)

    requires_research: bool = False
    requires_citations: bool = False
    requires_code: bool = False


class Plan(BaseModel):
    blog_title: str
    audience: str
    tone: str

    blog_kind: Literal[
        "explainer",
        "tutorial",
        "news_roundup",
        "comparison",
        "system_design",
    ] = "explainer"

    constraints: List[str] = Field(default_factory=list)

    tasks: List[Task]


# ============================================================
# Research Schemas
# ============================================================

class EvidenceItem(BaseModel):
    title: str
    url: str

    published_at: Optional[str] = None
    snippet: Optional[str] = None
    source: Optional[str] = None


class RouterDecision(BaseModel):
    needs_research: bool

    mode: Literal[
        "closed_book",
        "hybrid",
        "open_book",
    ]

    reason: str

    queries: List[str] = Field(default_factory=list)

    max_results_per_query: int = Field(default=5)


class EvidencePack(BaseModel):
    evidence: List[EvidenceItem] = Field(default_factory=list)


# ============================================================
# Image Planning Schemas
# ============================================================

class ImageSpec(BaseModel):
    placeholder: str = Field(
        ...,
        description="Placeholder such as [[IMAGE_1]]",
    )

    filename: str = Field(
        ...,
        description="Filename saved inside images/ folder.",
    )

    alt: str
    caption: str
    prompt: str

    size: Literal[
        "1024x1024",
        "1024x1536",
        "1536x1024",
    ] = "1024x1024"

    quality: Literal[
        "low",
        "medium",
        "high",
    ] = "medium"


class GlobalImagePlan(BaseModel):
    md_with_placeholders: str

    images: List[ImageSpec] = Field(default_factory=list)


# ============================================================
# LangGraph State
# ============================================================

class State(TypedDict):
    topic: str

    # Routing
    mode: str
    needs_research: bool
    queries: List[str]

    # Research
    evidence: List[EvidenceItem]

    # Blog Plan
    plan: Optional[Plan]

    # Recency
    as_of: str
    recency_days: int

    # Parallel Worker Output
    sections: Annotated[
        List[tuple[int, str]],
        operator.add,
    ]

    # Reducer
    merged_md: str
    md_with_placeholders: str
    image_specs: List[dict]

    # Final Output
    final: str