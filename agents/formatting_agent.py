# agents/formatting_agent.py

"""최종 보고서 포맷팅 및 저장 에이전트.

과제에서 자주 발생하는 실수는 Draft 생성 후 바로 END로 가는 것이다.
이 모듈은 초안을 받아 최종 보고서 파일을 명시적으로 저장하는 노드 역할을 한다.
"""
from __future__ import annotations
from utils.llm import get_llm


class FormattingAgent:
    """최종 보고서 스타일 정리 에이전트."""

    def __init__(self) -> None:
        self.llm = get_llm()

    def run(self, draft: str) -> str:
        print("[FormattingAgent] 최종 보고서 생성")

        prompt = f"""
아래 초안을 최종 제출용 보고서 형식으로 다듬어라.

요구사항:
- 문서는 마크다운 형식으로 작성한다.
- 최상단에 '# 기술 전략 분석 보고서' 제목을 둔다.
- SUMMARY는 1/2페이지 이내의 요약 톤으로 정리한다.
- 기술 현황 파트에서는 HBM4, PIM, CXL을 각각 소제목으로 분리한다.
- 경쟁사 동향 분석은 문장형으로 서술하되, 비교가 쉽게 드러나게 작성한다.
- 전략적 시사점은 '단기 / 중기 / 장기' 소제목으로 나누어 우선순위를 제시한다.
- REFERENCE는 실제 URL 목록을 bullet로 정리한다.
- 공개 정보 기반 추정의 한계와 TRL 4-6 구간의 불확실성을 명시한다.
- 지나치게 장황하지 않되, 발표/제출 모두 가능한 품질로 정리한다.

초안:
{draft}
"""
        return self.llm.invoke(prompt).content