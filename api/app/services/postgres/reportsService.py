import app.repository.postgres.reportsRepository as reports


def findAllReports():
    try:
        return reports.findAllReports()
    except Exception as e:
        print("[SERVICE] Error fetching reports:", e)
        raise e


def createReport(report):
    """
    Recebe um objeto Report e envia para o repository
    """
    try:
        return reports.createReport(report)
    except Exception as e:
        print("[SERVICE] Error creating report:", e)
        raise e


def findOneReport(report_id: str):
    try:
        return reports.findOneReport(report_id)
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
        return reports.updateReport(report_id, report_data)
    except Exception as e:
        print("[SERVICE] Error updating report:", e)
        raise e


def deleteReport(report_id: str):
    try:
        return reports.deleteReport(report_id)
    except Exception as e:
        print("[SERVICE] Error deleting report:", e)
        raise e
