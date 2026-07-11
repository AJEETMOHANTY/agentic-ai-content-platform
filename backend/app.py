# only graph creation

from langgraph.graph import StateGraph, START, END

from backend.state import State
from backend.router import router_node, route_next
from backend.research import research_node
from backend.orchestrator import orchestrator_node, fanout
from backend.worker import worker_node
from backend.reducer import reducer_subgraph


# ============================================================
# Build Main Graph
# ============================================================

g = StateGraph(State)

# Add Nodes
g.add_node("router", router_node)
g.add_node("research", research_node)
g.add_node("orchestrator", orchestrator_node)
g.add_node("worker", worker_node)
g.add_node("reducer", reducer_subgraph)

# Start
g.add_edge(START, "router")

# Router Decision
g.add_conditional_edges(
    "router",
    route_next,
    {
        "research": "research",
        "orchestrator": "orchestrator",
    },
)

# Research → Orchestrator
g.add_edge("research", "orchestrator")

# Fanout to Workers
g.add_conditional_edges(
    "orchestrator",
    fanout,
    ["worker"],
)

# Worker → Reducer
g.add_edge("worker", "reducer")

# End
g.add_edge("reducer", END)

# Compile Graph
app = g.compile()