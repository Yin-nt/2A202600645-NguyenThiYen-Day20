from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow


def test_workflow_produces_final_answer() -> None:
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))

    result = MultiAgentWorkflow().run(state)

    assert result.sources
    assert result.research_notes
    assert result.analysis_notes
    assert result.final_answer
    assert result.route_history[-1] == "done"
    assert not result.errors
