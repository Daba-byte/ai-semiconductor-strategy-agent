"""오픈소스 임베딩 후보군과 선정 기준을 정리하는 모듈.

현재 코드 실행에는 직접 쓰이지 않지만, 설계 산출물과 README에 반영하기 위해
후보 모델과 선정 기준을 구조화해 두었다.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class EmbeddingCandidate:
    name: str
    strengths: str
    limitations: str
    recommended_for: str


CANDIDATES: List[EmbeddingCandidate] = [
    EmbeddingCandidate(
        name='multilingual-e5-large',
        strengths='기술 문서 검색에 강하고 다국어 대응이 가능함',
        limitations='모델 크기가 커서 자원 요구량이 높을 수 있음',
        recommended_for='정확도 우선의 사내 문서/논문 검색',
    ),
    EmbeddingCandidate(
        name='bge-large-en',
        strengths='영문 semantic retrieval 품질이 우수함',
        limitations='한국어 비중이 높다면 성능 검토 필요',
        recommended_for='영문 논문/기사 중심 분석',
    ),
    EmbeddingCandidate(
        name='gte-large',
        strengths='성능과 속도의 균형이 좋음',
        limitations='최상위 성능보다는 실용적 균형에 가까움',
        recommended_for='빠른 프로토타입 구현',
    ),
]


def select_default_embedding() -> EmbeddingCandidate:
    """현재 기본 추천 모델을 반환한다."""
    return CANDIDATES[0]
