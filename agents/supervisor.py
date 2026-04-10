"""
Supervisor Agent

역할:
- 전체 워크플로를 통제한다.
- 검색/분석/초안/최종 포맷팅/저장/PDF 생성을 순차 수행한다.
- '초안 생성 후 바로 종료'하지 않고, 반드시 최종 포맷팅과 PDF 생성까지 진행한다.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from agents.competitor_analysis_agent import CompetitorAnalysisAgent
from agents.draft_generation_agent import DraftGenerationAgent
from agents.formatting_agent import FormattingAgent
from agents.retrieval_agent import RetrievalAgent
from agents.trl_analysis_agent import TRLAnalysisAgent
from agents.web_search_agent import WebSearchAgent
from utils.pdf_loader import load_pdfs
from utils.report_pdf import create_report_pdf
from utils.text_splitter import split_docs


class Supervisor:
    """전체 파이프라인 오케스트레이션 담당."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.outputs_dir = self.project_root / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)

        self.retrieval = RetrievalAgent()
        self.web = WebSearchAgent()
        self.trl = TRLAnalysisAgent()
        self.competitor = CompetitorAnalysisAgent()
        self.draft = DraftGenerationAgent()
        self.formatter = FormattingAgent()

    def run(self, query: str) -> Dict[str, str]:
        """전체 워크플로를 실행하고 결과 파일을 생성한다."""
        print("\n[Supervisor] Workflow 시작\n")

        docs = load_pdfs(self.project_root / "data" / "papers")
        chunks = split_docs(docs)
        self.retrieval.load_documents(chunks)

        retrieved_docs = self.retrieval.run(query=query, k=8)
        web_results = self.web.run(query=query, max_results=6)
        trl_result = self.trl.run(retrieved_docs=retrieved_docs, web_results=web_results)
        competitor_result = self.competitor.run(retrieved_docs=retrieved_docs, web_results=web_results)
        draft = self.draft.run(
            query=query,
            retrieved_docs=retrieved_docs,
            web_results=web_results,
            trl_result=trl_result,
            competitor_result=competitor_result,
        )
        final_report = self.formatter.run(draft=draft)

        markdown_path = self.outputs_dir / "final_report.md"
        pdf_path = self.outputs_dir / "final_report.pdf"
        context_path = self.outputs_dir / "run_context.json"

        markdown_path.write_text(final_report, encoding="utf-8")
        pdf_path = "outputs/final_report.pdf"

        create_report_pdf(
            markdown_text=final_report,
            output_path=pdf_path
        )
        
        context = {
            "query": query,
            "trl_result": trl_result,
            "competitor_result": competitor_result,
            "web_results": web_results,
            "retrieved_sources": [doc.metadata for doc in retrieved_docs],
        }
        context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

        print("\n[Supervisor] 완료\n")
        return {
            "report_text": final_report,
            "markdown_path": str(markdown_path),
            "pdf_path": str(pdf_path),
        }
