"""샘플 Retriever 평가 실행 파일.

현재는 작은 예시 QA set으로 성능 계산 과정을 보여주는 용도다.
"""
from __future__ import annotations

from evaluation.retriever_metrics import hit_rate_at_k, mean_reciprocal_rank


if __name__ == '__main__':
    # 각 질문에 대한 검색 결과 doc_id 순위 예시
    rank_lists = [
        ['hbm4_overview', 'skhynix_hbm', 'samsung_memory'],
        ['cxl_overview', 'micron_memory', 'hbm4_overview'],
        ['pim_overview', 'samsung_memory', 'cxl_overview'],
        ['samsung_memory', 'micron_memory', 'skhynix_hbm'],
    ]

    # 질문별 정답 문서 id 예시
    ground_truths = [
        'hbm4_overview',
        'cxl_overview',
        'pim_overview',
        'hbm4_overview',  # 마지막 문항은 일부러 미적중 예시를 줄 수 있다.
    ]

    hit_3 = hit_rate_at_k(rank_lists, ground_truths, k=3)
    mrr = mean_reciprocal_rank(rank_lists, ground_truths)

    print('=== Retriever Evaluation Sample ===')
    print(f'Hit Rate@3: {hit_3:.3f}')
    print(f'MRR: {mrr:.3f}')
