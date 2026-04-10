# evaluation/retrieval_eval.py

from agents.retrieval_agent import RetrievalAgent
from utils.pdf_loader import load_pdfs
from utils.text_splitter import split_docs
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# ======================
# QA SET (직접 만든다)
# ======================
qa_set = [
    {
        "question": "HBM4는 어떤 종류의 메모리 기술인가?",
        "keywords": ["HBM4", "high bandwidth", "memory"]
    },
    {
        "question": "HBM4의 주요 기술적 특징은 무엇인가?",
        "keywords": ["bandwidth", "stacked", "performance"]
    },
    {
        "question": "PIM 기술은 어떤 구조를 기반으로 하는가?",
        "keywords": ["processing in memory", "memory", "compute"]
    },
    {
        "question": "PIM 기술의 주요 장점은 무엇인가?",
        "keywords": ["data movement", "efficiency", "latency"]
    },
    {
        "question": "CXL 기술의 기본 목적은 무엇인가?",
        "keywords": ["memory expansion", "interconnect", "CXL"]
    },
    {
        "question": "CXL은 어떤 시스템에서 주로 활용되는가?",
        "keywords": ["server", "data center", "platform"]
    },
    {
        "question": "HBM 메모리는 기존 DRAM 대비 어떤 특징을 가지는가?",
        "keywords": ["bandwidth", "stacked", "high performance"]
    },
    {
        "question": "PIM 기술이 해결하려는 핵심 문제는 무엇인가?",
        "keywords": ["data movement", "bottleneck", "memory"]
    },
    {
        "question": "CXL 기반 메모리 확장의 장점은 무엇인가?",
        "keywords": ["scalability", "memory expansion", "flexibility"]
    },
    {
        "question": "HBM4의 개발 단계는 어느 수준에 있는가?",
        "keywords": ["production", "validation", "TRL"]
    },
    {
        "question": "HBM4와 PIM 기술을 비교했을 때 성숙도가 더 높은 기술은 무엇인가?",
        "keywords": ["HBM4", "production", "TRL", "mature"]
    },
    {
        "question": "데이터 이동 병목을 줄이기 위한 기술로 적합한 것은 무엇인가?",
        "keywords": ["PIM", "data movement", "processing"]
    },
    {
        "question": "대규모 데이터센터 환경에서 메모리 확장을 위해 적합한 기술은 무엇인가?",
        "keywords": ["CXL", "memory expansion", "server"]
    },
    {
        "question": "AI 연산 성능 향상을 위해 가장 직접적인 영향을 주는 메모리 기술은 무엇인가?",
        "keywords": ["HBM", "bandwidth", "performance"]
    },
    {
        "question": "PIM 기술이 상용화되기 어려운 이유는 무엇인가?",
        "keywords": ["validation", "prototype", "challenge"]
    },
    {
        "question": "CXL 기술이 기존 메모리 구조와 차별화되는 점은 무엇인가?",
        "keywords": ["interconnect", "scalability", "architecture"]
    },
    {
        "question": "HBM, PIM, CXL 중 장기적으로 통합 가능성이 높은 기술 방향은 무엇인가?",
        "keywords": ["integration", "architecture", "future"]
    },
]


# ======================
# 평가 함수
# ======================
def evaluate_retrieval(agent, qa_set, k=5):
    hit = 0
    mrr = 0

    for qa in qa_set:
        results = agent.run(query=qa["question"], k=k)

        found = False

        for idx, doc in enumerate(results):
            if any(keyword.lower() in doc.page_content.lower() for keyword in qa["keywords"]):
                hit += 1
                mrr += 1 / (idx + 1)
                found = True
                break

        if not found:
            mrr += 0

    hit_rate = hit / len(qa_set)
    mrr_score = mrr / len(qa_set)

    return hit_rate, mrr_score


# ======================
# 실행
# ======================
def main():
    project_root = Path(__file__).resolve().parent.parent

    retrieval = RetrievalAgent()

    docs = load_pdfs(project_root / "data" / "papers")
    chunks = split_docs(docs)

    retrieval.load_documents(chunks)

    hit, mrr = evaluate_retrieval(retrieval, qa_set, k=5)

    print("\n===== Retrieval Evaluation =====")
    print(f"Hit Rate@5: {hit:.2f}")
    print(f"MRR: {mrr:.2f}")


if __name__ == "__main__":
    main()