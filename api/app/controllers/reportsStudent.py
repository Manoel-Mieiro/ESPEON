from app.services.postgres import reportsStudentService
from app.dto.postgres.reports_student import ReportStudentDTO


def findAllStudentReports():
    try:
        return reportsStudentService.findAllStudentReports()
    except Exception as e:
        print("[CONTROLLER] Error fetching student reports:", e)
        raise e


def createStudentReport(data):
    try:
        rep_stu_dto = ReportStudentDTO(
            report_id=data["report_id"],
            user_id=data["user_id"],
            total_time_watched=data.get("total_time_watched"),
            attention_span=data.get("attention_span"),
            cam_enabled=data.get("cam_enabled", False),
            mic_enabled=data.get("mic_enabled", False),
            cam_streaming_span=data.get("cam_streaming_span"),
            mic_streaming_span=data.get("mic_streaming_span")
        )
        report_student = rep_stu_dto.to_standard()
        return reportsStudentService.createStudentReport(report_student)
    except Exception as e:
        print("[CONTROLLER] Error creating student report:", e)
        raise e


def findOneStudentReport(report_student_id):
    try:
        fetched = reportsStudentService.findOneStudentReport(report_student_id)
        if not fetched:
            raise Exception(f"Student report {report_student_id} não encontrado")
        return fetched
    except Exception as e:
        print("[CONTROLLER] Error fetching student report:", e)
        raise e


def updateStudentReport(report_student_id, data):
    try:
        rep_stu_dto = ReportStudentDTO(
            report_id=data["report_id"],
            user_id=data["user_id"],
            total_time_watched=data.get("total_time_watched"),
            attention_span=data.get("attention_span"),
            cam_enabled=data.get("cam_enabled", False),
            mic_enabled=data.get("mic_enabled", False),
            cam_streaming_span=data.get("cam_streaming_span"),
            mic_streaming_span=data.get("mic_streaming_span")
        )
        updated_report_student = rep_stu_dto.to_standard()
        return reportsStudentService.updateStudentReport(report_student_id, updated_report_student.to_dict())
    except Exception as e:
        print("[CONTROLLER] Error updating student report:", e)
        raise e


def deleteStudentReport(report_student_id):
    try:
        return reportsStudentService.deleteStudentReport(report_student_id)
    except Exception as e:
        print("[CONTROLLER] Error deleting student report:", e)
        raise e
