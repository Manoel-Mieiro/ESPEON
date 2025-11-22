from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from app.services.postgres.reports.pdf.style import (
    normal_style,
    section_style,
    subtitle_style,
    title_style
)


class ReportPdfFactory:
    def __init__(self, report):
        self.report = report
        self.buffer = BytesIO()
        self.c = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.x = 2 * cm
        self.y = self.height - 2 * cm

    def _draw_paragraph(self, text, style, spacing=0.2*cm):
        p = Paragraph(text, style)
        p.wrapOn(self.c, self.width - 4*cm, 2*cm)
        p.drawOn(self.c, self.x, self.y)
        self.y -= p.height + spacing

    def _draw_section(self, title, lines):
        self._draw_paragraph(title, section_style)
        for line in lines:
            self._draw_paragraph(line, normal_style)

    def generate(self):
        # Título
        self._draw_paragraph("Relatório da Aula", title_style, spacing=0.5*cm)
        self._draw_paragraph(
            self.report._lecture_alias or "Sem título", subtitle_style, spacing=0.5*cm)

        # Informações gerais
        info_lines = [
            f"Disciplina: {self.report._subject_name}",
            f"Docente: {self.report._teacher}",
            f"Total de alunos: {self.report._total_students}",
            # f"Tempo total assistido: {self.report._total_time_watched or 0:.0f} min",
            # f"Média de duração da aula: {self.report._avg_lecture_duration or 0:.0f} min",
            # f"Duração ociosa média: {self.report._avg_idle_duration or 0:.0f} min",
            # f"Atividade média (atenção): {self.report._avg_attention_span or 0:.0f} min"
        ]
        for line in info_lines:
            self._draw_paragraph(line, normal_style)

        # BASE
        base_lines = [
            f"Tempo total real de sessão: {getattr(self.report, '_real_total_session_duration', 0) or 0:.1f} min",
            f"Tempo médio por aluno: {getattr(self.report, '_avg_session_per_student', 0) or 0:.1f} min",
            f"Taxa de presença: {getattr(self.report, '_attendance_ratio', 0) or 0:.1%}"
        ]
        self._draw_section("BASE", base_lines)

        focus_lines = [
            f"Taxa de foco na aula: {getattr(self.report, '_lecture_focus_ratio', 0) or 0:.1%}",
            f"Duração média em foco: {getattr(self.report, '_avg_focus_duration', 0) or 0:.1f} min",
            f"Maior duração contínua focado: {getattr(self.report, '_max_focus_duration', 0) or 0:.1f} min"
        ]
        self._draw_section("FOCO", focus_lines)

        # DISTRAÇÃO
        distraction_lines = [
            f"Taxa de distração: {getattr(self.report, '_distraction_ratio', 0) or 0:.1%}",
            f"Frequência de distrações: {getattr(self.report, '_distraction_frequency', 0) or 0:.0f} eventos",
            f"Principais causas: {', '.join(getattr(self.report, '_main_distractions', []) or [])}"
        ]
        self._draw_section("DISTRAÇÃO", distraction_lines)

        # MULTITASKING
        fragmentation_lines = [
            f"Trocas de aba/janela: {getattr(self.report, '_tab_switch_frequency', 0) or 0:.0f} eventos",
            f"Intensidade de multitarefa: {getattr(self.report, '_multitasking_intensity', 0) or 0:.1%}",
            f"Fragmentação do foco: {getattr(self.report, '_focus_fragmentation', 0) or 0:.1%}",
        ]
        self._draw_section("MULTITASKING", fragmentation_lines)

        # ENGAJAMENTO
        engagement_lines = [
            f"Engajamento pela câmera: {getattr(self.report, '_camera_engagement', 0) or 0:.1%}",
            f"Engajamento pelo microfone: {getattr(self.report, '_mic_engagement', 0) or 0:.1%}",
            f"Participações voluntárias: {getattr(self.report, '_voluntary_participation', 0) or 0:.0f} interações",
        ]
        self._draw_section("ENGAJAMENTO", engagement_lines)

        trend = self.report._engagement_trend or {}
        trend_lines = [
                f"Engajamento Q1: {trend.get('q1', 0):.0%}",
                f"Engajamento Q2: {trend.get('q2', 0):.0%}",
                f"Engajamento Q3: {trend.get('q3', 0):.0%}",
                f"Engajamento Q4: {trend.get('q4', 0):.0%}",
                f"Pico de engajamento: {self.report._peak_engagement_time or 'N/A'}",
                f"Ponto de queda (50%): {self.report._dropoff_point or 'N/A'}"
            ]

        self._draw_section("PADRÕES TEMPORAIS", trend_lines)

        # MÉTRICAS COMPOSTAS DE ENGAJAMENTO
        score_lines = [
            f"Score geral de engajamento: {getattr(self.report, '_engagement_score', 0) or 0:.1%}",
            f"Saúde da atenção: {getattr(self.report, '_attention_health', 0) or 0:.1%}",
            f"Risco de distração: {getattr(self.report, '_distraction_risk', 0) or 0:.1%}",
        ]
        self._draw_section("SCORES", score_lines)

        # Rodapé
        self._draw_paragraph(
            f"Emitido em: {self.report._issued_at}", subtitle_style)

        # Finaliza PDF
        self.c.showPage()
        self.c.save()
        self.buffer.seek(0)
        return self.buffer
