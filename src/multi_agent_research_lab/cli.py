"""Command-line entrypoint for the lab starter."""

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.evaluation.benchmark import run_benchmark
from multi_agent_research_lab.evaluation.report import render_research_run_report
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging
from multi_agent_research_lab.services.llm_client import LLMClient

app = typer.Typer(help="Multi-Agent Research Lab starter CLI")
console = Console()


def _init() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run a minimal single-agent baseline placeholder."""

    _init()
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    response = LLMClient().complete(
        system_prompt="Answer as a single research agent.",
        user_prompt=f"Research and summarize this query: {request.query}",
    )
    state.final_answer = response.content
    console.print(Panel.fit(state.final_answer, title="Single-Agent Baseline"))


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow skeleton."""

    _init()
    workflow = MultiAgentWorkflow()
    result, metrics = run_benchmark(
        "multi-agent",
        query,
        lambda run_query: workflow.run(state=ResearchState(request=ResearchQuery(query=run_query))),
    )
    report_path = Path("reports") / "benchmark_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_research_run_report(result, metrics), encoding="utf-8")
    console.print(Panel.fit(str(report_path), title="Report Written"))
    console.print(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    app()
