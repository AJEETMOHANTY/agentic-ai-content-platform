# State TypedDict

import operator
from typing import Annotated, List, Optional, TypedDict

from backend.schemas import EvidenceItem, Plan


class State(TypedDict):
    topic: str

    # Router / Research
    mode: str
    needs_research: bool
    queries: List[str]
    evidence: List[EvidenceItem]
    plan: Optional[Plan]

    # Recency
    as_of: str
    recency_days: int

    # Worker Outputs
    sections: Annotated[List[tuple[int, str]], operator.add]

    # Reducer / Images
    merged_md: str
    md_with_placeholders: str
    image_specs: List[dict]

    # Final Output
    final: str