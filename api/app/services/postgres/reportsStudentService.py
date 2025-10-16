import app.repository.postgres.reportsStudentRepository as report_students


def findAllStudentReports():
    try:
        return report_students.findAllStudentReports()
    except Exception as e:
        print("[SERVICE] Error fetching student reports:", e)
        raise e


def createStudentReport(report_student):
    """
    Recebe um objeto ReportStudent e envia para o repository
    """
    try:
        return report_students.createStudentReport(report_student)
    except Exception as e:
        print("[SERVICE] Error creating student report:", e)
        raise e


def findOneStudentReport(report_student_id: str):
    try:
        return report_students.findOneStudentReport(report_student_id)
    except Exception as e:
        print("[SERVICE] Error fetching student report:", e)
        raise e


def updateStudentReport(report_student_id: str, report_student_data):
    """
    Recebe um dicionário ou um objeto ReportStudent, envia para o repository
    """
    try:
        if hasattr(report_student_data, "to_dict"):
            report_student_data = report_student_data.to_dict()
        return report_students.updateStudentReport(report_student_id, report_student_data)
    except Exception as e:
        print("[SERVICE] Error updating student report:", e)
        raise e


def deleteStudentReport(report_student_id: str):
    try:
        return report_students.deleteStudentReport(report_student_id)
    except Exception as e:
        print("[SERVICE] Error deleting student report:", e)
        raise e
