from evaluation.retriever_metrics import hit_rate_at_k, mean_reciprocal_rank


def test_metrics_basic():
    rank_lists = [
        ['a', 'b', 'c'],
        ['x', 'y', 'z'],
    ]
    ground_truths = ['a', 'z']

    assert hit_rate_at_k(rank_lists, ground_truths, k=1) == 0.5
    assert round(mean_reciprocal_rank(rank_lists, ground_truths), 3) == 0.667
