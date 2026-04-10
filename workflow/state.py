"""Workflow 전체에서 공유하는 상태 객체.

LangGraph를 쓰는 경우 TypedDict 또는 Pydantic 모델로 바꿔도 되지만,
여기서는 파이썬 표준 dataclass로 쉽게 이해할 수 있게 작성했다.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class WorkflowState:
    """에이전트 간에 전달되는 공통 상태."""

    query: str
    retrieved_docs: List[Dict[str, Any]] = field(default_factory=list)
    web_results: List[Dict[str, Any]] = field(default_factory=list)
    trl_summary: Dict[str, Any] = field(default_factory=dict)
    competitor_summary: Dict[str, Any] = field(default_factory=dict)
    draft_report: str = ''
    final_report: str = ''
