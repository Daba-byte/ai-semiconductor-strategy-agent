"""Workflow orchestration 모듈.

실제 LangGraph를 사용하지 않더라도, 어떤 순서로 Agent가 연결되는지
한 파일에서 명확히 볼 수 있도록 구성했다.
"""
from __future__ import annotations

from agents.competitor_analysis_agent import CompetitorAnalysisAgent
from agents.draft_generation_agent import DraftGenerationAgent
from agents.formatting_agent import FormattingAgent
from agents.retrieval_agent import RetrievalAgent
from agents.supervisor import Supervisor
from agents.trl_analysis_agent import TRLAnalysisAgent
from agents.web_search_agent import WebSearchAgent
from utils.logger import log
from workflow.state import WorkflowState


class SemiconductorAnalysisWorkflow:
    """반도체 기술 전략 분석 Workflow 실행기."""

    def __init__(self) -> None:
        self.supervisor = Supervisor()
        self.retrieval_agent = RetrievalAgent()
        self.web_search_agent = WebSearchAgent()
        self.trl_agent = TRLAnalysisAgent()
        self.competitor_agent = CompetitorAnalysisAgent()
        self.draft_agent = DraftGenerationAgent()
        self.formatting_agent = FormattingAgent()

    def run(self, query: str) -> WorkflowState:
        """전체 Workflow를 실행하고 최종 상태를 반환한다."""
        state = WorkflowState(query=query)

        log('Workflow: 실행 시작')

        # 1) 내부 문서 검색
        state.retrieved_docs = self.retrieval_agent.run(query)

        # 2) 웹 검색 수행
        state.web_results = self.web_search_agent.run(query)

        # 3) TRL 추정
        state.trl_summary = self.trl_agent.run(state.retrieved_docs, state.web_results)

        # 4) 경쟁사 비교 분석
        state.competitor_summary = self.competitor_agent.run(state.retrieved_docs, state.web_results)

        # 5) 초안 생성
        state.draft_report = self.draft_agent.run(
            query=state.query,
            retrieved_docs=state.retrieved_docs,
            web_results=state.web_results,
            trl_summary=state.trl_summary,
            competitor_summary=state.competitor_summary,
        )

        # 6) 초안 저장
        self.formatting_agent.save_draft(state.draft_report)

        # 7) Supervisor 검증
        if not self.supervisor.validate_draft(state):
            raise RuntimeError('초안 검증에 실패했습니다. 검색 결과와 초안 내용을 확인하세요.')

        # 8) 최종 보고서 저장
        final_path = self.formatting_agent.save_final(state.draft_report)
        state.final_report = final_path.read_text(encoding='utf-8')

        log('Workflow: 실행 종료')
        return state
