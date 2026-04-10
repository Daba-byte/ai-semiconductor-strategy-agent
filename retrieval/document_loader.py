"""샘플 문서를 로드하는 모듈.

현재는 data/sample_docs 폴더의 markdown 파일을 읽어오기만 한다.
향후 PDF 파서, 웹 문서 수집기, DB 저장소 등으로 쉽게 확장할 수 있다.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Document:
    """검색 대상 문서를 표현하는 최소 단위."""

    doc_id: str
    title: str
    content: str
    source: str


class DocumentLoader:
    """샘플 문서 디렉터리에서 문서를 읽어온다."""

    def __init__(self, docs_dir: str = 'data/sample_docs') -> None:
        self.docs_dir = Path(docs_dir)

    def load(self) -> List[Document]:
        """docs_dir 아래의 markdown 파일을 모두 읽어 Document 리스트로 반환한다."""
        documents: List[Document] = []
        for path in sorted(self.docs_dir.glob('*.md')):
            content = path.read_text(encoding='utf-8')
            documents.append(
                Document(
                    doc_id=path.stem,
                    title=path.stem.replace('_', ' ').title(),
                    content=content,
                    source=str(path),
                )
            )
        return documents
