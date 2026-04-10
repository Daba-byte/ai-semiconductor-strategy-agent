"""프로젝트 전역 설정을 관리하는 모듈.

환경변수(.env)를 읽어서 실행 옵션을 파싱한다.
처음 보는 사람도 알 수 있도록 설정 이름을 명확하게 유지했다.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# .env 파일이 있으면 자동 로드한다.
load_dotenv()


@dataclass
class Settings:
    """실행 시 필요한 설정값 묶음."""

    use_mock_web_search: bool = os.getenv('USE_MOCK_WEB_SEARCH', 'true').lower() == 'true'
    top_k: int = int(os.getenv('TOP_K', '3'))
    openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
    tavily_api_key: str = os.getenv('TAVILY_API_KEY', '')
    serpapi_api_key: str = os.getenv('SERPAPI_API_KEY', '')


settings = Settings()
