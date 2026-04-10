"""
Text Splitter

역할:
- PDF 페이지 단위 문서를 chunk 단위로 나눈다.
- chunk_size / overlap은 기술 문서 검색에 맞춰 보수적으로 설정했다.
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_docs(docs: List[Document]) -> List[Document]:
    """문서를 검색 가능한 chunk로 나눈다."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"[Splitter] 총 {len(chunks)} chunks 생성")
    return chunks
