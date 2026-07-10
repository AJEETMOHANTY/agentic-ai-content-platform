from __future__ import annotations

from datetime import date, timedelta
from typing import List

from langchain_core.messages import HumanMessage, SystemMessage

from .config import llm
from .prompts import ROUTER_SYSTEM, RESEARCH_SYSTEM
from .schemas import (
    State,
    RouterDecision,
    EvidencePack,
    EvidenceItem,
)
from .utils import tavily_search, iso_to_date

# ============================================================
# Router Node
# ============================================================


def router_node(state: State) -> dict:
    """
    Decide whether the blog requires web research before planning.
    """

    decider = llm.with_structured_output(RouterDecision)

    decision = decider.invoke(
        [
            SystemMessage(content=ROUTER_SYSTEM),
            HumanMessage(
                content=(f"Topic: {state['topic']}\n" f"As-of date: {state['as_of']}")
            ),
        ]
    )

    if decision.mode == "open_book":
        recency_days = 7
    elif decision.mode == "hybrid":
        recency_days = 45
    else:
        recency_days = 3650

    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
        "recency_days": recency_days,
    }


# ============================================================
# Conditional Edge
# ============================================================


def route_next(state: State) -> str:
    """
    Decide whether to continue with research or planning.
    """

    if state["needs_research"]:
        return "research"

    return "orchestrator"


# ============================================================
# Research Node
# ============================================================


def research_node(state: State) -> dict:
    """
    Perform Tavily web search and extract structured evidence.
    """

    queries = (state.get("queries") or [])[:10]

    raw_results: List[dict] = []

    for query in queries:
        raw_results.extend(
            tavily_search(
                query=query,
                max_results=6,
            )
        )

    if not raw_results:
        return {"evidence": []}

    extractor = llm.with_structured_output(EvidencePack)

    evidence_pack = extractor.invoke(
        [
            SystemMessage(content=RESEARCH_SYSTEM),
            HumanMessage(
                content=(
                    f"As-of date: {state['as_of']}\n"
                    f"Recency days: {state['recency_days']}\n\n"
                    f"Raw Results:\n{raw_results}"
                )
            ),
        ]
    )

    deduplicated = {}

    for evidence in evidence_pack.evidence:
        if evidence.url:
            deduplicated[evidence.url] = evidence

    evidence = list(deduplicated.values())

    # Filter recent articles for open-book mode
    if state.get("mode") == "open_book":

        current_date = date.fromisoformat(state["as_of"])

        cutoff_date = current_date - timedelta(days=int(state["recency_days"]))

        evidence = [
            item
            for item in evidence
            if (
                (parsed_date := iso_to_date(item.published_at))
                and parsed_date >= cutoff_date
            )
        ]

    return {"evidence": evidence}
