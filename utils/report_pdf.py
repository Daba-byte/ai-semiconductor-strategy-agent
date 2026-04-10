# utils/report_pdf.py

"""
고급 PDF 생성 모듈
- Markdown 제거
- 제목/섹션/본문 스타일 적용
- 한글 폰트 지원
"""

import re
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm


# ======================
# 1. 한글 폰트 등록
# ======================
def _register_korean_font():
    font_name = "NotoSansKR"
    font_path = "fonts/NotoSansKR-Regular.ttf"

    if not os.path.exists(font_path):
        raise FileNotFoundError(
            f"폰트 파일이 없습니다: {font_path}\n"
            "→ fonts 폴더에 NotoSansKR-Regular.ttf 넣어주세요"
        )

    pdfmetrics.registerFont(TTFont(font_name, font_path))
    return font_name


# ======================
# 2. Markdown 정리
# ======================
def _clean_markdown(text):
    # bold 제거
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # heading 제거
    text = re.sub(r"#+\s*", "", text)

    # 링크 제거
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)

    return text


# ======================
# 3. 스타일 정의
# ======================
def _build_styles(font_name):
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=base["Heading1"],
        fontName=font_name,
        fontSize=18,
        leading=22,
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=base["Heading2"],
        fontName=font_name,
        fontSize=14,
        leading=18,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontName=font_name,
        fontSize=10,
        leading=14,
        spaceAfter=4,
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=base["Normal"],
        fontName=font_name,
        fontSize=10,
        leading=14,
        leftIndent=10,
        spaceAfter=2,
    )

    return title_style, heading_style, body_style, bullet_style


# ======================
# 4. 라인 파싱
# ======================
def _parse_lines(lines):
    parsed = []

    for line in lines:
        line = line.strip()

        if not line:
            parsed.append(("space", ""))
            continue

        # SUMMARY / 섹션
        if line.upper().startswith("SUMMARY"):
            parsed.append(("title", line))
        elif line.startswith("##"):
            parsed.append(("heading", line.replace("##", "").strip()))
        elif line.startswith("- "):
            parsed.append(("bullet", line[2:]))
        else:
            parsed.append(("body", line))

    return parsed


# ======================
# 5. PDF 생성
# ======================
def create_report_pdf(markdown_text, output_path="outputs/final_report.pdf"):

    print("[PDF] 생성 시작")

    # 폰트 등록
    font_name = _register_korean_font()

    # Markdown 제거
    clean_text = _clean_markdown(markdown_text)

    # 스타일 생성
    title_style, heading_style, body_style, bullet_style = _build_styles(font_name)

    # 문서 설정
    doc = SimpleDocTemplate(
        output_path,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    content = []

    # 줄 단위 파싱
    lines = clean_text.split("\n")
    parsed_lines = _parse_lines(lines)

    for kind, text in parsed_lines:

        if kind == "title":
            content.append(Paragraph(text, title_style))
            content.append(Spacer(1, 10))

        elif kind == "heading":
            content.append(Paragraph(text, heading_style))
            content.append(Spacer(1, 6))

        elif kind == "bullet":
            content.append(Paragraph(f"• {text}", bullet_style))

        elif kind == "body":
            content.append(Paragraph(text, body_style))

        elif kind == "space":
            content.append(Spacer(1, 6))

    doc.build(content)

    print(f"[PDF] 생성 완료: {output_path}")