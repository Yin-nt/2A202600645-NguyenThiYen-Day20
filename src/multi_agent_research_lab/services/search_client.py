"""Search client abstraction for ResearcherAgent."""

from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client with a deterministic local fallback."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Return local mock documents relevant to a query.

        The lab can later replace this method with Tavily, Bing, SerpAPI, or an
        internal document store without changing agent code.
        """

        normalized = " ".join(query.strip().split())
        topics = [
            "định nghĩa bài toán và chia nhỏ nhiệm vụ",
            "thiết kế vai trò agent và hợp đồng handoff",
            "guardrail, trace và đánh giá",
            "so sánh single-agent và multi-agent",
            "failure mode và chiến lược khắc phục",
        ]
        return [
            SourceDocument(
                title=f"Ghi chú nghiên cứu local {index}: {topic}",
                url=f"local://research/{index}",
                snippet=(
                    f"Với truy vấn '{normalized}', tập trung vào {topic}. Ghi lại bằng chứng, "
                    "giả định, rủi ro và tiêu chí đánh giá có thể đo được."
                ),
                metadata={"rank": index, "provider": "local_mock"},
            )
            for index, topic in enumerate(topics[:max_results], start=1)
        ]
