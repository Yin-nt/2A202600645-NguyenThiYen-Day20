"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and derive simple quality/cost metrics."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    citation_score = min(3.0, len(state.sources) * 0.6)
    completeness_score = sum(
        [
            2.0 if state.research_notes else 0.0,
            2.0 if state.analysis_notes else 0.0,
            2.0 if state.final_answer else 0.0,
            1.0 if not state.errors else 0.0,
        ]
    )
    quality_score = min(10.0, citation_score + completeness_score)
    estimated_cost = sum(
        result.metadata.get("cost_usd", 0.0) or 0.0 for result in state.agent_results
    )
    notes = (
        f"{len(state.sources)} nguồn, {len(state.errors)} lỗi, "
        f"{len(state.route_history)} quyết định route"
    )
    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        estimated_cost_usd=estimated_cost,
        quality_score=quality_score,
        notes=notes,
    )
    return state, metrics
