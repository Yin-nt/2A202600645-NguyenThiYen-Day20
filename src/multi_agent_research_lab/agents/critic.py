"""Optional critic agent for bonus work."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings."""

        findings: list[str] = []
        if not state.final_answer:
            findings.append("Final answer is missing.")
        if state.final_answer and state.sources and "[1]" not in state.final_answer:
            findings.append("Final answer may not expose source references clearly.")
        if not state.errors and not findings:
            findings.append("No blocking quality issues found.")

        content = "\n".join(f"- {finding}" for finding in findings)
        state.add_trace_event(self.name, {"finding_count": len(findings)})
        state.agent_results.append(
            AgentResult(agent=AgentName.CRITIC, content=content, metadata={"finding_count": len(findings)})
        )
        return state
