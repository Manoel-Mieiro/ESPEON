from app.services.postgres import reportsService
from app.dto.postgres.reports import ReportDTO


def findAllReports():
    try:
        return reportsService.findAllReports()
    except Exception as e:
        print("[CONTROLLER] Error fetching reports:", e)
        raise e


def createReport(data):
    try:
        rep_dto = ReportDTO(
            lecture_id=data["lecture_id"],
            subject_id=data["subject_id"],
            total_students=data.get("total_students", 0),
            total_time_watched=data.get("total_time_watched", 0),
            avg_lecture_duration=data.get("avg_lecture_duration"),
            avg_idle_duration=data.get("avg_idle_duration"),
            avg_attention_span=data.get("avg_attention_span"),
            pct_enabled_camera=data.get("pct_enabled_camera"),
            pct_enabled_mic=data.get("pct_enabled_mic"),
            avg_cam_streaming_span=data.get("avg_cam_streaming_span"),
            avg_mic_streaming_span=data.get("avg_mic_streaming_span")
        )
        report = rep_dto.to_standard()
        return reportsService.createReport(report)
    except Exception as e:
        print("[CONTROLLER] Error creating report:", e)
        raise e


def findOneReport(report_id):
    try:
        fetched = reportsService.findOneReport(report_id)
        if not fetched:
            raise Exception(f"Report {report_id} não encontrado")
        return fetched
    except Exception as e:
        print("[CONTROLLER] Error fetching report:", e)
        raise e


def updateReport(report_id, data):
    try:
        rep_dto = ReportDTO(
            lecture_id=data["lecture_id"],
            subject_id=data["subject_id"],
            total_students=data.get("total_students", 0),
            total_time_watched=data.get("total_time_watched", 0),
            avg_lecture_duration=data.get("avg_lecture_duration"),
            avg_idle_duration=data.get("avg_idle_duration"),
            avg_attention_span=data.get("avg_attention_span"),
            pct_enabled_camera=data.get("pct_enabled_camera"),
            pct_enabled_mic=data.get("pct_enabled_mic"),
            avg_cam_streaming_span=data.get("avg_cam_streaming_span"),
            avg_mic_streaming_span=data.get("avg_mic_streaming_span")
        )
        updated_report = rep_dto.to_standard()
        return reportsService.updateReport(report_id, updated_report.to_dict())
    except Exception as e:
        print("[CONTROLLER] Error updating report:", e)
        raise e


def deleteReport(report_id):
    try:
        return reportsService.deleteReport(report_id)
    except Exception as e:
        print("[CONTROLLER] Error deleting report:", e)
        raise e
