"""Writer agent."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or LLMClient()

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`."""

        if not state.analysis_notes:
            message = "Writer skipped because analysis_notes is empty."
            state.errors.append(message)
            state.add_trace_event(self.name, {"status": "skipped", "reason": message})
            return state

        citations = ", ".join(
            f"[{index}] {source.title}" for index, source in enumerate(state.sources, start=1)
        )
        prompt = (
            f"Câu hỏi: {state.request.query}\n\n"
            f"Ghi chú nghiên cứu:\n{state.research_notes}\n\n"
            f"Phân tích:\n{state.analysis_notes}\n\n"
            f"Trích dẫn: {citations or 'Chưa thu thập source'}"
        )
        response = self.llm_client.complete(
            system_prompt="Viết câu trả lời nghiên cứu ngắn gọn, có bằng chứng và caveat.",
            user_prompt=prompt,
        )
        state.final_answer = response.content
        state.add_trace_event(
            self.name,
            {
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
                "cost_usd": response.cost_usd,
            },
        )
        state.agent_results.append(
            AgentResult(
                agent=AgentName.WRITER,
                content=state.final_answer,
                metadata={
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "cost_usd": response.cost_usd,
                },
            )
        )
        return state
