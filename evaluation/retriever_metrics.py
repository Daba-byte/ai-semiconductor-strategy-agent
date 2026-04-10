"""Retriever 성능 평가 지표 구현.

Hit Rate@K와 MRR 계산 함수를 별도로 분리해 두면,
README나 실험 노트북에서 재사용하기 좋다.
"""
from __future__ import annotations

from typing import Iterable, List


def hit_rate_at_k(rank_lists: List[List[str]], ground_truths: List[str], k: int) -> float:
    """상위 K개 안에 정답 문서가 등장한 비율을 계산한다.

    rank_lists: 각 질문의 검색 결과 문서 id 리스트
    ground_truths: 각 질문의 정답 문서 id
    """
    if len(rank_lists) != len(ground_truths):
        raise ValueError('rank_lists와 ground_truths의 길이가 다릅니다.')

    hit_count = 0
    for ranked_docs, gt in zip(rank_lists, ground_truths):
        if gt in ranked_docs[:k]:
            hit_count += 1
    return hit_count / len(ground_truths) if ground_truths else 0.0



def mean_reciprocal_rank(rank_lists: List[List[str]], ground_truths: List[str]) -> float:
    """MRR(Mean Reciprocal Rank)를 계산한다."""
    if len(rank_lists) != len(ground_truths):
        raise ValueError('rank_lists와 ground_truths의 길이가 다릅니다.')

    reciprocal_ranks = []
    for ranked_docs, gt in zip(rank_lists, ground_truths):
        rr = 0.0
        for idx, doc_id in enumerate(ranked_docs, start=1):
            if doc_id == gt:
                rr = 1.0 / idx
                break
        reciprocal_ranks.append(rr)

    return sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0
