"""
Draft Generation Agent

역할:
- RAG 결과, 웹 검색 결과, TRL 분석, 경쟁사 분석을 묶어 초안을 생성한다.
- 단순 요약이 아니라 '왜 지금 분석해야 하는지', '어디에 투자해야 하는지'까지 포함하도록 프롬프트를 설계한다.
"""

from __future__ import annotations
from typing import Any, Dict, List
from langchain_core.documents import Document
from utils.llm import get_llm


class DraftGenerationAgent:
    """LLM 기반 보고서 초안 생성기."""

    def __init__(self) -> None:
        self.llm = get_llm()

    def run(
        self,
        query: str,
        retrieved_docs: List[Document],
        web_results: List[Dict[str, Any]],
        trl_result: Dict[str, Dict[str, str]],
        competitor_result: Dict[str, Dict[str, str]],
    ) -> str:
        print("[DraftGenerationAgent] 초안 생성")

        rag_text = "\n\n".join(
            [
                f"[문서{i}] source={doc.metadata.get('source', 'unknown')} | page={doc.metadata.get('page', 'unknown')}\n{doc.page_content[:1500]}"
                for i, doc in enumerate(retrieved_docs, start=1)
            ]
        )

        web_text = "\n\n".join(
            [
                f"[웹{i}] title={item['title']}\nsummary={item['content']}\nurl={item['url']}\ndomain={item['domain']}\npublished_date={item.get('published_date', 'unknown')}"
                for i, item in enumerate(web_results, start=1)
            ]
        )

        prompt = f"""
당신은 반도체 R&D 전략 보고서를 작성하는 수석 분석가다.
아래 정보를 바탕으로 '기술 전략 분석 보고서 초안'을 한국어로 작성하라.

[사용자 목표]
{query}

[내부 문서 검색 결과]
{rag_text}

[웹 검색 결과]
{web_text}

[TRL 초안]
{trl_result}

[경쟁사 분석 초안]
{competitor_result}

반드시 아래 요구를 지켜라.
1. 보고서 구조는 SUMMARY, 분석 배경, 기술 현황, 경쟁사 동향 분석, 전략적 시사점, REFERENCE 순서로 작성한다.
2. HBM4, PIM, CXL 각각의 기술 집중 이유를 분리해서 설명한다.
3. TRL은 반드시 '수준 + 근거 + 한계'를 함께 쓴다.
4. 경쟁사별 비교는 삼성전자, SK hynix, Micron을 포함한다.
5. 전략적 시사점에는 단기/중기/장기 우선순위를 넣는다.
6. REFERENCE에는 실제 URL을 리스트업한다.
7. 과장하지 말고, 공개 정보 기반 추정이라는 점을 명확히 써라.
8. 너무 짧지 않게, 바로 보고서로 쓸 수 있을 정도로 구체적으로 작성한다.

반드시 아래를 포함하라:

1. TRL 비교 표 (Markdown table 형식)
2. 경쟁사 비교 표 (Markdown table 형식)
3. 전략 우선순위 표 (Markdown table 형식)

표 형식 예시:
| 항목 | 값 |
|------|----|
| A | B |

텍스트 설명을 부가로 작성하고 필수적인 표로 정리하라.
"""

        return self.llm.invoke(prompt).content
