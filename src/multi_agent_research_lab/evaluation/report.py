"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown."""

    lines = [
        "# Báo Cáo Benchmark",
        "",
        "Báo cáo này so sánh các runner theo latency, estimated cost, quality và ghi chú.",
        "",
        "| Run | Latency (s) | Cost (USD) | Quality | Ghi chú |",
        "|---|---:|---:|---:|---|",
    ]
    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"{item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}"
        lines.append(f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | {item.notes} |")
    lines.extend(
        [
            "",
            "## Failure Modes",
            "",
            "- Search coverage có thể yếu khi dùng local mock provider.",
            "- Fallback deterministic dễ kiểm tra nhưng không tự nhiên bằng LLM thật.",
            "- Guardrail `MAX_ITERATIONS` giúp chặn workflow chạy vô hạn.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_research_run_report(state: ResearchState, metrics: BenchmarkMetrics | None = None) -> str:
    """Render one completed research run with analysis and trace details."""

    lines = [
        "# Báo Cáo Benchmark",
        "",
        "## Câu Hỏi",
        "",
        state.request.query,
        "",
        "## Câu Trả Lời Cuối Cùng",
        "",
        state.final_answer or "Chưa tạo câu trả lời cuối cùng.",
        "",
        "## Phân Tích",
        "",
        state.analysis_notes or "Chưa tạo analysis notes.",
        "",
        "## Trace",
        "",
        "| Bước | Event | Chi tiết |",
        "|---:|---|---|",
    ]
    for index, event in enumerate(state.trace, start=1):
        details = str(event.get("payload", {})).replace("|", "\\|")
        lines.append(f"| {index} | {event.get('name', '')} | `{details}` |")

    lines.extend(
        [
            "",
            "## Lịch Sử Route",
            "",
            " -> ".join(state.route_history) or "Chưa ghi nhận route.",
            "",
            "## Nguồn",
            "",
        ]
    )
    for index, source in enumerate(state.sources, start=1):
        url = f" ({source.url})" if source.url else ""
        lines.append(f"{index}. {source.title}{url}: {source.snippet}")

    if metrics is not None:
        lines.extend(
            [
                "",
                "## Chỉ Số",
                "",
                f"- Latency: {metrics.latency_seconds:.2f}s",
                f"- Cost: {metrics.estimated_cost_usd if metrics.estimated_cost_usd is not None else 'n/a'}",
                f"- Quality: {metrics.quality_score if metrics.quality_score is not None else 'n/a'}",
                f"- Ghi chú: {metrics.notes}",
            ]
        )

    lines.extend(
        [
            "",
            "## Lỗi Tiềm Ẩn Và Cách Khắc Phục",
            "",
            "Local mock search provider có thể bỏ sót bằng chứng thực tế. Khi chạy production, "
            "hãy thay `SearchClient` bằng Tavily, Bing, SerpAPI hoặc internal corpus client.",
        ]
    )
    return "\n".join(lines) + "\n"
