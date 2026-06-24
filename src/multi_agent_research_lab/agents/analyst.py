"""Analyst agent."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`."""

        if not state.research_notes:
            message = "Analyst skipped because research_notes is empty."
            state.errors.append(message)
            state.add_trace_event(self.name, {"status": "skipped", "reason": message})
            return state

        source_count = len(state.sources)
        state.analysis_notes = "\n".join(
            [
                "Các luận điểm chính:",
                f"- Truy vấn nên được chia thành các phần việc theo vai trò cho {state.request.audience}.",
                f"- Phân tích nên dựa trên {source_count} nguồn đã thu thập.",
                "- Thiết kế tốt nhất cần có field handoff rõ ràng: sources, notes, analysis, answer.",
                "Rủi ro:",
                "- Search coverage yếu có thể làm final answer quá tự tin.",
                "- Thiếu giới hạn vòng lặp có thể khiến agent chạy vô hạn.",
                "Khuyến nghị đánh giá:",
                "- So sánh latency, citation coverage, error rate và điểm quality từ người review.",
            ]
        )
        state.add_trace_event(self.name, {"source_count": source_count})
        state.agent_results.append(
            AgentResult(
                agent=AgentName.ANALYST,
                content=state.analysis_notes,
                metadata={"source_count": source_count},
            )
        )
        return state
