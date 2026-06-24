"""Supervisor / router."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route."""

        settings = get_settings()
        if state.iteration >= settings.max_iterations:
            route = "done"
            reason = "đã đạt max_iterations"
        elif not state.research_notes:
            route = "researcher"
            reason = "thiếu research notes"
        elif not state.analysis_notes:
            route = "analyst"
            reason = "thiếu analysis notes"
        elif not state.final_answer:
            route = "writer"
            reason = "thiếu final answer"
        else:
            route = "done"
            reason = "đã hoàn thành đầy đủ deliverables"

        state.record_route(route)
        state.add_trace_event(self.name, {"route": route, "reason": reason})
        state.agent_results.append(
            AgentResult(
                agent=AgentName.SUPERVISOR,
                content=f"Route tiếp theo: {route}",
                metadata={"reason": reason, "iteration": state.iteration},
            )
        )
        return state
