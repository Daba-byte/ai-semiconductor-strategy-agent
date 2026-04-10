"""
LLM 유틸리티

역할:
- OpenAI Chat 모델을 일관되게 생성한다.
- 모델명은 .env에서 OPENAI_MODEL로 바꿀 수 있다.
"""

from __future__ import annotations
import os
from langchain_openai import ChatOpenAI


def get_llm() -> ChatOpenAI:
    """공통 ChatOpenAI 인스턴스를 반환한다."""
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model_name, temperature=0.2)
