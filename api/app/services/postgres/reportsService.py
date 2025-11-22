from app.services.postgres.reports.metricsCalc.participation import (
    calculate_camera_engagement,
    calculate_mic_engagement,
    calculate_voluntary_participation,
)

from app.services.postgres.reports.metricsCalc.time import (
    calculate_dropoff_point,
    calculate_peak_engagement_time,
    calculate_engagement_trend,
)

from app.services.postgres.reports.metricsCalc.base import (
    calculate_real_total_session_duration,
    calculate_real_avg_session_per_student,
    calculate_attendance_ratio,
)

from app.services.postgres.reports.metricsCalc.disturb import (
    calculate_main_distractions,
    calculate_distraction_frequency,
    calculate_distraction_ratio,
)

from app.services.postgres.reports.metricsCalc.multitasking import (
    calculate_tab_switch_frequency,
    calculate_multitasking_intensity,
    calculate_focus_fragmentation,
)

from app.services.postgres.reports.metricsCalc.focus import (
    calculate_lecture_focus_ratio,
    calculate_focus_durations,
)

from app.services.postgres.reports.metrics import (
    calculateTotalStudents,
    calculateTotalTimeWatched,
    calculateAvgLectureDuration,
    calculateCameraMicUsage,
    calculateAvgIdle,
    calculateAvgAttentionSpan,
    getIdleMinMax,
    getAttentionSpanMinMax
)
from datetime import datetime
from app.models.postgres.reports import Report
import app.repository.postgres.reportsRepository as reportsRepository
import app.repository.tracesRepository as tracesRepository
import os

flask_port = os.getenv("FLASK_RUN_PORT", "8183")


def fetchLectureTraces(lecture_id: str):
    """
    Busca os traces de uma aula e retorna o JSON diretamente.

    Args:
        lecture_id (str): ID da aula

    Returns:
        list: lista de traces da aula
    """
    try:
        traces = tracesRepository.findOneTraceByLecture(lecture_id)
        return traces
    except Exception as e:
        print(
            f"[SERVICE] Erro ao buscar traces para lecture_id={lecture_id}: {e}")
        return []


"""
CRUDS
"""


def findAllReports():
    try:
        return reportsRepository.findAllReports()
    except Exception as e:
        print("[SERVICE] Error fetching reports:", e)
        raise e


def createReport(report: Report):
    """
    Cria ou atualiza o relatório de uma aula (lecture_id único).
    """
    try:
        existing_report = reportsRepository.getReportByLectureId(
            report._lecture_id)

        if existing_report:
            print(
                f"[SERVICE] Relatório já existe para lecture_id={report._lecture_id}. Atualizando issued_at...")
            updated = reportsRepository.updateReport(existing_report["report_id"], {
                "issued_at": datetime.utcnow()
            })
            return updated

        print(
            f"[SERVICE] Criando novo relatório para lecture_id={report._lecture_id}...")
        return reportsRepository.createReport(report)

    except Exception as e:
        print("[SERVICE] Error creating report:", e)
        raise e


def findOneReport(report_id: str):
    try:
        report, extras = reportsRepository.findOneReport(report_id)
        final = populateReportMetrics(report)
        result = final.to_dict()
        result.update(extras)
        return result
    except Exception as e:
        print("[SERVICE] Error fetching report:", e)
        raise e


def updateReport(report_id: str, report_data):
    """
    Recebe um dicionário ou um objeto Report, envia para o repository
    """
    try:
        if hasattr(report_data, "to_dict"):
            report_data = report_data.to_dict()
        return reportsRepository.updateReport(report_id, report_data)
    except Exception as e:
        print("[SERVICE] Error updating report:", e)
        raise e


def deleteReport(report_id: str):
    try:
        return reportsRepository.deleteReport(report_id)
    except Exception as e:
        print("[SERVICE] Error deleting report:", e)
        raise e


def populateReportMetrics(report: object):
    traces = fetchLectureTraces(report._lecture_id)

    metrics = {}

    metrics['total_students'] = calculateTotalStudents(traces)

    # 1. Métricas base
    metrics['real_total_session_duration'] = calculate_real_total_session_duration(
        traces)
    metrics['avg_session_per_student'] = calculate_real_avg_session_per_student(
        traces)
    metrics['attendance_ratio'] = calculate_attendance_ratio(
        traces, report._lecture_id)

    # 2. Métricas de Foco
    metrics['lecture_focus_ratio'] = calculate_lecture_focus_ratio(traces)
    metrics['avg_focus_duration'], metrics['max_focus_duration'] = calculate_focus_durations(
        traces)

    # 3. Métricas de Distração
    metrics['distraction_ratio'] = calculate_distraction_ratio(traces)
    metrics['distraction_frequency'] = calculate_distraction_frequency(traces)
    metrics['main_distractions'] = calculate_main_distractions(traces)

    # 4. Métricas de Multitasking
    metrics['tab_switch_frequency'] = calculate_tab_switch_frequency(traces)
    metrics['multitasking_intensity'] = calculate_multitasking_intensity(
        traces)
    metrics['focus_fragmentation'] = calculate_focus_fragmentation(traces)

    # 5. Métricas de Participação Ativa
    metrics['camera_engagement'] = calculate_camera_engagement(traces)
    metrics['mic_engagement'] = calculate_mic_engagement(traces)
    metrics['voluntary_participation'] = calculate_voluntary_participation(
        traces)
    
    # 5. Métricas temporais
    metrics['engagement_trend'] = calculate_engagement_trend(traces, report._lecture_id)
    metrics['peak_engagement_time'] = calculate_peak_engagement_time(traces, report._lecture_id)
    metrics['dropoff_point'] = calculate_dropoff_point(traces, report._lecture_id)


    metrics['total_time_watched'] = calculateTotalTimeWatched(
        report._lecture_id)
    metrics['avg_lecture_duration'] = calculateAvgLectureDuration(
        report._subject_id)
    metrics['pct_enabled_camera'], metrics['pct_enabled_mic'] = calculateCameraMicUsage(
        traces)
    metrics['avg_idle_duration'] = calculateAvgIdle(traces)
    metrics['avg_attention_span'] = calculateAvgAttentionSpan(
        traces,
        metrics['total_time_watched'],
        metrics['total_students'],
        metrics['avg_idle_duration']
    )
    metrics['min_idle_duration'], metrics['max_idle_duration'] = getIdleMinMax(
        traces)
    metrics['min_attention_span'], metrics['max_attention_span'] = getAttentionSpanMinMax(
        traces,
        metrics['total_time_watched'],
        metrics['total_students']
    )
    metrics['lecture_alias'] = traces[0].get("classTitle") if traces else None

    for k, v in metrics.items():
        setattr(report, f"_{k}", v)

    return report
