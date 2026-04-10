"""오프라인 데모용 간단한 키워드 기반 Retriever.

scikit-learn 같은 외부 의존성 없이도 실행되도록 직접 구현한 버전이다.
실제 과제에서는 이 자리를 FAISS, BM25, Hybrid Retrieval 등으로 교체하면 된다.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Dict, List
import re

from retrieval.document_loader import Document


@dataclass
class RetrievalResult:
    """검색 결과 1건을 표현하는 자료구조."""

    doc_id: str
    title: str
    score: float
    source: str
    content: str


class SimpleKeywordRetriever:
    """문서를 토큰화한 뒤 query와의 겹침 정도를 점수화한다."""

    def __init__(self, documents: List[Document]) -> None:
        if not documents:
            raise ValueError('검색할 문서가 비어 있습니다.')
        self.documents = documents
        self.doc_tokens = [self._tokenize(doc.content + ' ' + doc.title) for doc in documents]

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        # 한글/영문/숫자만 남기고 소문자 기준으로 나눈다.
        text = text.lower()
        tokens = re.findall(r'[가-힣a-z0-9]+', text)
        return tokens

    def _score(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        # 매우 단순한 코사인 유사도 유사 점수.
        # term frequency만 사용하고, 오프라인 데모가 목적이다.
        q_freq: Dict[str, int] = {}
        d_freq: Dict[str, int] = {}
        for t in query_tokens:
            q_freq[t] = q_freq.get(t, 0) + 1
        for t in doc_tokens:
            d_freq[t] = d_freq.get(t, 0) + 1

        common = set(q_freq) & set(d_freq)
        dot = sum(q_freq[t] * d_freq[t] for t in common)
        q_norm = sqrt(sum(v * v for v in q_freq.values()))
        d_norm = sqrt(sum(v * v for v in d_freq.values()))
        if q_norm == 0 or d_norm == 0:
            return 0.0
        return dot / (q_norm * d_norm)

    def search(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        query_tokens = self._tokenize(query)
        scored = []
        for doc, tokens in zip(self.documents, self.doc_tokens):
            score = self._score(query_tokens, tokens)
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)

        results: List[RetrievalResult] = []
        for score, doc in scored[:top_k]:
            results.append(
                RetrievalResult(
                    doc_id=doc.doc_id,
                    title=doc.title,
                    score=float(score),
                    source=doc.source,
                    content=doc.content,
                )
            )
        return results
