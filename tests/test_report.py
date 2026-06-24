from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.evaluation.report import render_markdown_report, render_research_run_report


def test_report_renders_markdown() -> None:
    report = render_markdown_report([BenchmarkMetrics(run_name="baseline", latency_seconds=1.23)])
    assert "Báo Cáo Benchmark" in report
    assert "baseline" in report


def test_research_run_report_includes_analysis_and_trace() -> None:
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))
    state.analysis_notes = "Analysis content"
    state.final_answer = "Answer content"
    state.add_trace_event("supervisor", {"route": "researcher"})

    report = render_research_run_report(state)

    assert "## Phân Tích" in report
    assert "Analysis content" in report
    assert "## Trace" in report
    assert "supervisor" in report
