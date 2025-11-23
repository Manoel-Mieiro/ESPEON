from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

styles = getSampleStyleSheet()

# Estilos
title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=16,
    leading=18,
    spaceAfter=6,
    alignment=TA_LEFT
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    underline=True,
    fontSize=12,
    leading=14,
    spaceAfter=10,
    alignment=TA_LEFT,
    wordWrap='CJK'
)

footer_style = ParagraphStyle(
    name="footer",
    parent=styles['Normal'],
    alignment=TA_RIGHT,
    fontSize=9
)

section_style = ParagraphStyle(
    'Section',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=16,
    spaceBefore=8,
    spaceAfter=4,
    alignment=TA_LEFT
)

normal_style = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=12,
    leading=14,
    spaceAfter=2
)