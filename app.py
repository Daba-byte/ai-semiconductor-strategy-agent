"""프로젝트 실행 진입점.
실행 순서:
1) .env 파일 준비
2) data/papers 폴더에 PDF 논문 배치
3) python3 app.py 실행

결과물:
- outputs/final_report.md
- outputs/final_report.pdf
- outputs/run_context.json
"""
from pathlib import Path
from agents.supervisor import Supervisor
from dotenv import load_dotenv
load_dotenv()

def main() -> None:
    """전체 워크플로를 실행하고 최종 산출물을 저장한다."""
    load_dotenv()

    project_root = Path(__file__).resolve().parent
    query = "HBM4, PIM, CXL 관련 최신 반도체 R&D 동향을 분석하고 경쟁사별 기술 성숙도와 위협 수준을 비교해 기술 전략 분석 보고서를 작성하라."

    supervisor = Supervisor(project_root=project_root)
    result = supervisor.run(query=query)

    print("\n===== 최종 보고서 저장 완료 =====\n")
    print(f"Markdown: {result['markdown_path']}")
    print(f"PDF: {result['pdf_path']}")
    print("\n===== 보고서 미리보기 =====\n")
    print(result["report_text"][:3000])


if __name__ == "__main__":
    main()
