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
        existing_report = reportsRepository.getReportByLectureId(report._lecture_id)

        if existing_report:
            print(f"[SERVICE] Relatório já existe para lecture_id={report._lecture_id}. Atualizando issued_at...")
            updated = reportsRepository.updateReport(existing_report["report_id"], {
                "issued_at": datetime.utcnow()
            })
            return updated

        print(f"[SERVICE] Criando novo relatório para lecture_id={report._lecture_id}...")
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
