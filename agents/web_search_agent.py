"""
Web Search Agent

역할:
- Tavily REST API를 직접 호출해 최신 웹 검색 결과를 수집한다.
- 별도 파이썬 패키지 의존성을 줄이기 위해 requests 기반으로 구현했다.
- 확증 편향을 줄이기 위해 다양한 도메인 결과를 수집/기록한다.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

import requests


class WebSearchAgent:
    """Tavily API를 직접 호출하는 웹 검색 에이전트."""

    TAVILY_URL = "https://api.tavily.com/search"

    def __init__(self) -> None:
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY가 설정되지 않았습니다.")

    def run(self, query: str, max_results: int = 6) -> List[Dict[str, Any]]:
        """실제 웹 검색을 수행하고 핵심 필드만 정리해 반환한다."""
        print(f"[WebSearchAgent] 실제 웹 검색 실행: {query}")

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "topic": "news",
            "include_answer": False,
            "include_raw_content": False,
        }
        response = requests.post(self.TAVILY_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        results: List[Dict[str, Any]] = []
        domains = set()

        for item in data.get("results", []):
            url = item.get("url", "")
            domain = url.split("/")[2] if url.startswith("http") and len(url.split("/")) > 2 else "unknown"
            domains.add(domain)
            results.append(
                {
                    "title": item.get("title", "제목 없음"),
                    "content": item.get("content", "요약 없음"),
                    "url": url,
                    "domain": domain,
                    "published_date": item.get("published_date", "unknown"),
                }
            )

        print(f"[WebSearchAgent] 수집된 source 수: {len(results)}")
        print(f"[WebSearchAgent] 고유 도메인 수: {len(domains)}")
        return results
