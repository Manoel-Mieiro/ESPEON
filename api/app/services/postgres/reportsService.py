from app.utils.time_utils import (
    get_current_datetime, convert_time_objects_to_string)
from app.services.postgres.reports.metricsCalc.participation import (
    calculate_camera_engagement,
    calculate_mic_engagement,
    calculate_voluntary_participation,
)

from app.services.postgres.reports.metricsCalc.scores import (
    calculate_distraction_risk,
    calculate_attention_health,
    calculate_engagement_score,
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
from datetime import datetime, time, date
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
        reports_data = reportsRepository.findAllReports()

        if not reports_data:
            return []

        processed_reports = []
        for report_data in reports_data:
            try:

                report_obj = Report.from_dict(report_data)

                populated_report = populateReportMetrics(report_obj)

                report_dict = populated_report.to_dict()

                processed_reports.append(report_dict)

            except Exception as e:
                print(f"[SERVICE] Error processing report: {e}")
                processed_reports.append(
                    convert_time_objects_to_string(report_data))

        return processed_reports

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
                f"[SERVICE] Relatório já existe para lecture_id={report._lecture_id}. Atualizando métricas...")

            populated_report = populateReportMetrics(report)

            update_data = {
                "issued_at": get_current_datetime(),
                "total_students": populated_report._total_students,
                "lecture_length": populated_report._lecture_length,
                "avg_session_per_student": populated_report._avg_session_per_student,
                "attendance_ratio": populated_report._attendance_ratio,
                "lecture_focus_ratio": populated_report._lecture_focus_ratio,
                "avg_focus_duration": populated_report._avg_focus_duration,
                "max_focus_duration": populated_report._max_focus_duration,
                "distraction_ratio": populated_report._distraction_ratio,
                "distraction_frequency": populated_report._distraction_frequency,
                "main_distractions": populated_report._main_distractions or [],
                "tab_switch_frequency": populated_report._tab_switch_frequency,
                "multitasking_intensity": populated_report._multitasking_intensity,
                "focus_fragmentation": populated_report._focus_fragmentation,
                "camera_engagement": populated_report._camera_engagement,
                "mic_engagement": populated_report._mic_engagement,
                "voluntary_participation": populated_report._voluntary_participation,
                "engagement_trend": populated_report._engagement_trend or {},
                "peak_engagement_time": populated_report._peak_engagement_time,
                "dropoff_point": populated_report._dropoff_point,
                "engagement_score": populated_report._engagement_score,
                "attention_health": populated_report._attention_health,
                "distraction_risk": populated_report._distraction_risk,
                "lecture_alias": populated_report._lecture_alias,
                "subject_name": populated_report._subject_name,
                "teacher": populated_report._teacher
            }

            update_data = {k: v for k, v in update_data.items()
                           if v is not None}

            print("[DEBUG] Checking for time objects before conversion:")
            for key, value in update_data.items():
                if isinstance(value, (datetime, time, date)):
                    print(
                        f"  Found time object at {key}: {value} (type: {type(value)})")

            update_data = convert_time_objects_to_string(update_data)

            print("[DEBUG] After conversion:")
            for key, value in update_data.items():
                if any(time_type in str(type(value)) for time_type in ['time', 'datetime', 'date']):
                    print(
                        f"  STILL time object at {key}: {value} (type: {type(value)})")

            updated = reportsRepository.updateReport(
                existing_report["report_id"], update_data)
            return updated

        print(
            f"[SERVICE] Criando novo relatório para lecture_id={report._lecture_id}...")

        populated_report = populateReportMetrics(report)

        if not populated_report._issued_at:
            populated_report._issued_at = get_current_datetime()

        return reportsRepository.createReport(populated_report)

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
    metrics['lecture_length'] = calculateTotalTimeWatched(report._lecture_id)
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

    # 6. Métricas temporais
    metrics['engagement_trend'] = calculate_engagement_trend(
        traces, report._lecture_id)
    metrics['peak_engagement_time'] = calculate_peak_engagement_time(
        traces, report._lecture_id)
    metrics['dropoff_point'] = calculate_dropoff_point(
        traces, report._lecture_id)

    # 7. Scores Compostos
    metrics['engagement_score'] = calculate_engagement_score(metrics)
    metrics['attention_health'] = calculate_attention_health(metrics)
    metrics['distraction_risk'] = calculate_distraction_risk(metrics)

    metrics['lecture_alias'] = traces[0].get("classTitle") if traces else None

    for k, v in metrics.items():
        setattr(report, f"_{k}", v)

    return report
