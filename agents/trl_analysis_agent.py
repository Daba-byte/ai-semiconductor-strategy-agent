"""
TRL Analysis Agent

역할:
- 검색된 문서와 웹 결과를 바탕으로 기술 성숙도(TRL)를 추정한다.
- TRL 4-6 구간은 공개 정보로 완전 검증이 어렵기 때문에,
  그 한계를 보고서에 함께 명시할 수 있도록 근거 문장을 남긴다.
"""

from __future__ import annotations

from typing import Any, Dict, List

from langchain_core.documents import Document


class TRLAnalysisAgent:
    """규칙 기반 1차 TRL 초안 생성기."""

    def run(self, retrieved_docs: List[Document], web_results: List[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
        print("[TRLAnalysisAgent] TRL 분석 수행")

        joined_docs = " ".join(doc.page_content for doc in retrieved_docs).lower()
        joined_web = " ".join((item.get("title", "") + " " + item.get("content", "")) for item in web_results).lower()
        corpus = f"{joined_docs} {joined_web}"

        return {
            "HBM4": self._estimate_hbm4(corpus),
            "PIM": self._estimate_pim(corpus),
            "CXL": self._estimate_cxl(corpus),
        }

    def _estimate_hbm4(self, corpus: str) -> Dict[str, str]:
        if any(keyword in corpus for keyword in ["sample", "qualification", "production", "mass production", "12hi"]):
            return {
                "level": "TRL 7-8",
                "reason": "샘플 공급, 제품 검증, 양산 준비 관련 표현이 확인되어 시제품 검증 이후 단계로 추정된다.",
                "confidence": "medium",
            }
        return {
            "level": "TRL 6-7",
            "reason": "기술/제품 발표는 활발하지만 실제 양산/고객 공급 정보가 제한적이어서 시스템 시연 단계로 추정된다.",
            "confidence": "low-medium",
        }

    def _estimate_pim(self, corpus: str) -> Dict[str, str]:
        if any(keyword in corpus for keyword in ["prototype", "accelerator", "fpga", "benchmark"]):
            return {
                "level": "TRL 4-5",
                "reason": "논문, 시뮬레이션, 프로토타입 검증 중심이므로 연구 및 초기 실증 단계로 판단된다.",
                "confidence": "medium",
            }
        return {
            "level": "TRL 3-4",
            "reason": "개념 검증 수준의 공개 정보가 주를 이뤄 초기 기술 성숙 단계로 판단된다.",
            "confidence": "low",
        }

    def _estimate_cxl(self, corpus: str) -> Dict[str, str]:
        if any(keyword in corpus for keyword in ["memory expander", "server", "deployment", "platform"]):
            return {
                "level": "TRL 6-7",
                "reason": "서버/플랫폼 수준의 실증 및 상용화 준비 움직임이 확인되어 시스템 시연 단계로 추정된다.",
                "confidence": "medium",
            }
        return {
            "level": "TRL 5-6",
            "reason": "기술 공개는 활발하지만 실운용 정보는 제한적이어서 유사 환경 통합 테스트 단계로 판단된다.",
            "confidence": "low-medium",
        }
