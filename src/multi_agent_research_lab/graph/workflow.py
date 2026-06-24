"""Multi-agent workflow orchestration."""

from multi_agent_research_lab.agents import AnalystAgent, ResearcherAgent, SupervisorAgent, WriterAgent
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.observability.tracing import trace_span


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def __init__(
        self,
        supervisor: SupervisorAgent | None = None,
        researcher: ResearcherAgent | None = None,
        analyst: AnalystAgent | None = None,
        writer: WriterAgent | None = None,
    ) -> None:
        self.supervisor = supervisor or SupervisorAgent()
        self.agents = {
            "researcher": researcher or ResearcherAgent(),
            "analyst": analyst or AnalystAgent(),
            "writer": writer or WriterAgent(),
        }

    def build(self) -> object:
        """Return a simple graph description for inspection."""

        return {
            "nodes": ["supervisor", *self.agents.keys(), "done"],
            "edges": {
                "supervisor": [*self.agents.keys(), "done"],
                "researcher": ["supervisor"],
                "analyst": ["supervisor"],
                "writer": ["supervisor"],
            },
        }

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""

        settings = get_settings()
        with trace_span("multi_agent_workflow", {"query": state.request.query}) as span:
            while state.iteration < settings.max_iterations:
                state = self.supervisor.run(state)
                route = state.route_history[-1]
                if route == "done":
                    break

                agent = self.agents.get(route)
                if agent is None:
                    state.errors.append(f"Unknown route: {route}")
                    state.add_trace_event("workflow", {"status": "error", "route": route})
                    break

                state = agent.run(state)
            else:
                state.errors.append("Workflow stopped after reaching max_iterations.")

        state.add_trace_event("workflow", span)
        return state
