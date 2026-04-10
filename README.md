# AI Mini Project - Semiconductor Technology Strategy Analyzer

HBM4, PIM, CXL 관련 최신 반도체 R&D 정보를 수집하고, 기술 성숙도(TRL)와 경쟁사 위협 수준을 분석하여 최종 보고서를 자동 생성하는 Agentic Workflow 프로젝트입니다.

이 프로젝트는 단순 요약기가 아니라, 다음 흐름을 하나의 파이프라인으로 연결합니다.

- PDF 논문/자료 로딩
- 문서 chunking 및 벡터 검색(RAG)
- 최신 웹 검색(Tavily)
- TRL 추정
- 경쟁사 분석
- LLM 기반 보고서 생성
- 제출용 PDF 자동 생성

## 1. 프로젝트 개요

이 시스템은 Supervisor 패턴을 기반으로 설계되었습니다. 각 Agent는 역할이 분리되어 있으며, Supervisor가 전체 실행 순서를 통제합니다. 특히 초안 생성 이후 바로 종료하지 않고, 최종 포맷팅과 PDF 저장까지 반드시 수행하도록 설계했습니다.

### Workflow 요약

1. `data/papers` 폴더의 PDF 논문/자료를 불러옵니다.
2. 문서를 chunk로 분할하고 FAISS 인덱스를 생성합니다.
3. 사용자 질의에 대해 내부 문서 RAG 검색을 수행합니다.
4. Tavily API를 통해 최신 웹 검색을 수행합니다.
5. 문서 + 웹 결과를 바탕으로 기술별 TRL을 추정합니다.
6. 경쟁사별 위협 수준을 분석합니다.
7. 초안 생성 Agent가 보고서 초안을 작성합니다.
8. Formatting Agent가 최종 제출용 마크다운을 생성합니다.
9. 보고서를 `outputs/final_report.md`와 `outputs/final_report.pdf`로 저장합니다.

## 2. 폴더 구조

```text
ai-mini-dev-v2/
├── agents/
│   ├── competitor_analysis_agent.py
│   ├── draft_generation_agent.py
│   ├── formatting_agent.py
│   ├── retrieval_agent.py
│   ├── supervisor.py
│   ├── trl_analysis_agent.py
│   └── web_search_agent.py
├── utils/
│   ├── llm.py
│   ├── pdf_loader.py
│   ├── report_pdf.py
│   └── text_splitter.py
├── data/
│   └── papers/
│       └── (여기에 PDF 논문 배치)
├── outputs/
│   └── (실행 결과 저장)
├── .env.example
├── app.py
├── requirements.txt
└── README.md
```

## 3. 가상환경 세팅

macOS / Linux 기준입니다.

```bash
cd ai-mini-dev-v2
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

가상환경이 정상적으로 활성화되면 터미널 앞에 `(.venv)`가 표시됩니다.

## 4. 환경 변수 설정

`.env.example`을 복사해서 `.env` 파일을 만듭니다.

```bash
cp .env.example .env
```

그리고 아래 값을 실제 키로 바꿉니다.

```env
OPENAI_API_KEY=sk-your-openai-key
TAVILY_API_KEY=tvly-your-tavily-key
OPENAI_MODEL=gpt-4o-mini
```

### 필요한 키 설명

- `OPENAI_API_KEY`: OpenAI Embeddings + Chat 모델 호출용
- `TAVILY_API_KEY`: 최신 웹 검색용
- `OPENAI_MODEL`: 기본 모델명. 바꾸지 않으면 `gpt-4o-mini`를 사용합니다.

## 5. 논문 넣는 위치

반드시 PDF 파일을 아래 위치에 넣어야 합니다.

```text
data/papers/
```

예시:

```text
data/papers/
├── 01_hbm4_system.pdf
├── 02_pim_architecture.pdf
├── 03_cxl_memory_expansion.pdf
├── 04_pim_vs_cxl.pdf
└── 05_market_report.pdf
```

문서 수가 많을수록 검색 품질이 좋아지지만, 너무 불필요한 문서가 섞이면 결과가 흔들릴 수 있으므로 주제 관련도가 높은 논문과 기술 기사 중심으로 구성하는 것이 좋습니다.

## 6. 실행 방법

```bash
python3 app.py
```

정상 실행되면 아래 흐름이 출력됩니다.

```text
[Supervisor] Workflow 시작
[PDF Loader] 총 N 페이지 로드
[Splitter] 총 N chunks 생성
[RetrievalAgent] 벡터스토어 생성
[RetrievalAgent] 질의 검색 수행 (top-8)
[WebSearchAgent] 실제 웹 검색 실행
[TRLAnalysisAgent] TRL 분석 수행
[CompetitorAnalysisAgent] 경쟁사 분석 수행
[DraftGenerationAgent] 초안 생성
[FormattingAgent] 최종 보고서 생성
[Supervisor] 완료
```

## 7. 실행 결과

실행이 끝나면 아래 파일이 생성됩니다.

```text
outputs/
├── final_report.md
├── final_report.pdf
└── run_context.json
```

### 파일 설명

- `final_report.md`: 최종 보고서 마크다운 버전
- `final_report.pdf`: 제출용 PDF 버전
- `run_context.json`: 웹 검색 결과, TRL 분석 결과, 검색 출처 메타데이터 저장

## 8. Agent 설명

### RetrievalAgent
문서 chunk를 임베딩하여 FAISS 인덱스를 만들고 관련 문서를 검색합니다. 즉, 이 프로젝트의 RAG 검색 부분을 담당합니다.

### WebSearchAgent
Tavily REST API를 직접 호출해 최신 웹 검색 결과를 수집합니다. 별도 Tavily 파이썬 패키지를 강제하지 않고 `requests`로 호출하도록 작성했습니다.

### TRLAnalysisAgent
공개 정보 기반으로 기술 성숙도를 1차 추정합니다. 특히 TRL 4-6 구간은 추정 오차 가능성이 높다는 점을 보고서에서 명시할 수 있도록 근거 문장을 함께 만듭니다.

### CompetitorAnalysisAgent
삼성전자, SK hynix, Micron의 기술 집중 영역과 위협 수준을 정리합니다.

### DraftGenerationAgent
문서 검색 결과, 웹 검색 결과, TRL, 경쟁사 분석을 통합하여 전략 보고서 초안을 생성합니다.

### FormattingAgent
초안을 최종 제출용 문서 형식으로 다듬습니다. 최종적으로 마크다운과 PDF 모두 생성 가능합니다.

### Supervisor
전체 실행 순서를 통제하는 최상위 Agent입니다. 설계 실수로 자주 발생하는 "초안만 만들고 종료" 문제를 막기 위해, 반드시 최종 포맷팅과 PDF 생성까지 진행합니다.

## 9. 품질 향상 포인트

현재 코드만으로도 과제 제출은 가능하지만, 아래 항목을 추가하면 완성도가 더 올라갑니다.

- Retrieval 평가 코드 추가 (`Hit Rate@K`, `MRR`)
- 웹 검색 결과 필터링 강화 (도메인 신뢰도 기준)
- 경쟁사별 Threat Score를 정량표로 추가
- 보고서 내 표/도표 자동 생성
- 결과 PDF에 표지 페이지 추가

## 10. 자주 나는 오류와 해결

### 1) `OPENAI_API_KEY` 관련 오류
`.env` 파일을 만들지 않았거나 값이 비어 있는 경우입니다.

```bash
cat .env
```

으로 확인하세요.

### 2) `Could not import faiss`
아래처럼 재설치하세요.

```bash
python3 -m pip install faiss-cpu==1.7.4
```

### 3) `PDF 파일이 없습니다`
`data/papers` 폴더에 실제 PDF를 넣었는지 확인하세요.

### 4) `TAVILY_API_KEY` 관련 오류
Tavily API 키가 없거나 잘못 설정된 경우입니다.

## 11. 발표/시연용 한 줄 설명

> 본 시스템은 HBM4, PIM, CXL 관련 내부 문서 검색과 최신 웹 검색을 결합한 Agentic RAG 기반 기술 전략 분석 시스템으로, 경쟁사 동향과 TRL 추정을 통합하여 최종 보고서를 자동 생성합니다.
