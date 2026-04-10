# agents/retrieval_agent.py
"""문서 검색 에이전트.

내부 문서나 사내 지식 저장소를 검색하는 역할을 가정한다.
현재는 샘플 markdown 문서를 간단한 키워드 기반 retriever로 검색한다.
"""
from __future__ import annotations

from typing import List

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


class RetrievalAgent:
    """논문/보고서 chunk 검색을 담당하는 에이전트."""

    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore: FAISS | None = None

    def load_documents(self, chunks: List[Document]) -> None:
        """문서 chunk 목록으로 벡터스토어를 생성한다."""
        if not chunks:
            raise ValueError("로드할 chunk가 없습니다. data/papers 폴더를 확인하세요.")

        print("[RetrievalAgent] 벡터스토어 생성")
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)

    def run(self, query: str, k: int = 8) -> List[Document]:
        """질의와 가장 유사한 문서를 반환한다."""
        if self.vectorstore is None:
            raise RuntimeError("vectorstore가 아직 생성되지 않았습니다. load_documents()를 먼저 호출하세요.")

        print(f"[RetrievalAgent] 질의 검색 수행 (top-{k})")
        return self.vectorstore.similarity_search(query, k=k)
