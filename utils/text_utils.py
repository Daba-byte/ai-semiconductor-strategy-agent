"""텍스트 정리용 유틸 함수 모음."""
from __future__ import annotations

import re
from typing import Iterable


def normalize_whitespace(text: str) -> str:
    """여러 줄/여러 공백을 정리해 읽기 좋은 문자열로 만든다."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def join_paragraphs(lines: Iterable[str]) -> str:
    """문장 리스트를 문단 하나처럼 결합한다."""
    return normalize_whitespace(' '.join(lines))
