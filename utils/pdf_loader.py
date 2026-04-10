"""
PDF Loader

역할:
- data/papers 폴더의 모든 PDF를 읽는다.
- 각 페이지를 LangChain Document 형태로 반환한다.
- source 파일명과 page 정보를 metadata에 보존한다.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdfs(folder_path: Path) -> List[Document]:
    """폴더 내 PDF를 모두 불러온다."""
    if not folder_path.exists():
        raise FileNotFoundError(f"PDF 폴더가 존재하지 않습니다: {folder_path}")

    all_docs: List[Document] = []
    pdf_files = sorted(folder_path.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"PDF 파일이 없습니다. {folder_path} 폴더에 논문을 넣어주세요.")

    for pdf_file in pdf_files:
        loader = PyPDFLoader(str(pdf_file))
        pages = loader.load()
        for page in pages:
            page.metadata["source"] = pdf_file.name
        all_docs.extend(pages)

    print(f"[PDF Loader] 총 {len(all_docs)} 페이지 로드")
    return all_docs
