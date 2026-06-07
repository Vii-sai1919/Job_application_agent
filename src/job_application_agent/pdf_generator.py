from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

DARK = colors.HexColor('#1E3A5F')
ACCENT = colors.HexColor('#2E86C1')
GRAY = colors.HexColor('#555555')
LIGHT = colors.HexColor('#F4F6F8')

def generate_resume_pdf(text_content: str, output_path: str, candidate_name: str = "Candidate"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        'Name',
        fontSize=24,
        textColor=DARK,
        fontName='Helvetica-Bold',
        spaceAfter=4,
        alignment=TA_CENTER
    )
    section_style = ParagraphStyle(
        'Section',
        fontSize=11,
        textColor=ACCENT,
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=4,
        textTransform='uppercase'
    )
    body_style = ParagraphStyle(
        'Body',
        fontSize=10,
        textColor=GRAY,
        fontName='Helvetica',
        spaceAfter=4,
        leading=15
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        fontSize=10,
        textColor=GRAY,
        fontName='Helvetica',
        spaceAfter=3,
        leading=14,
        leftIndent=12,
        bulletIndent=0
    )

    story = []
    lines = text_content.strip().split('\n')

    # Name as header
    story.append(Paragraph(candidate_name, name_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=8))

    section_keywords = [
        'education', 'skills', 'experience', 'projects',
        'achievements', 'extracurricular', 'position', 'objective',
        'summary', 'contact', 'academic'
    ]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
            continue

        lower = stripped.lower()

        # Skip if it's just the candidate name repeated
        if stripped.lower() == candidate_name.lower():
            continue

        # Section headers
        if any(kw in lower for kw in section_keywords) and len(stripped) < 50 and stripped.isupper():
            story.append(Paragraph(stripped, section_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=4))

        # Bullet points
        elif stripped.startswith('•') or stripped.startswith('-') or stripped.startswith('*'):
            clean = stripped.lstrip('•-* ').strip()
            story.append(Paragraph(f"• {clean}", bullet_style))

        # Bold headers (short lines that look like job titles)
        elif len(stripped) < 60 and stripped.endswith(':'):
            story.append(Paragraph(f"<b>{stripped}</b>", body_style))

        else:
            story.append(Paragraph(stripped, body_style))

    doc.build(story)
    return output_path


def generate_cover_letter_pdf(text_content: str, output_path: str, candidate_name: str = "Candidate"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=25*mm,
        leftMargin=25*mm,
        topMargin=25*mm,
        bottomMargin=25*mm
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        'Header',
        fontSize=14,
        textColor=DARK,
        fontName='Helvetica-Bold',
        spaceAfter=2,
        alignment=TA_LEFT
    )
    body_style = ParagraphStyle(
        'Body',
        fontSize=11,
        textColor=GRAY,
        fontName='Helvetica',
        spaceAfter=10,
        leading=18
    )

    story = []
    story.append(Paragraph(candidate_name, header_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=16))

    for para in text_content.strip().split('\n\n'):
        clean = para.strip()
        if clean:
            story.append(Paragraph(clean, body_style))
            story.append(Spacer(1, 6))

    doc.build(story)
    return output_path