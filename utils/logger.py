"""간단한 로그 출력을 담당하는 유틸리티.

실제 실무에서는 logging 모듈을 더 정교하게 구성할 수 있다.
"""
from __future__ import annotations

from datetime import datetime


def log(message: str) -> None:
    """현재 시간을 포함해 로그를 출력한다."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{now}] {message}')
