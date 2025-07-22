import app.services.reports.reports as reportService

def listReports(kind):
    try:
        return reportService.findAllReports(kind)
    except Exception as e:
        print("[CONTROLLER]Error fetching reports:", e)
        raise e


def createReports(kind, subject=None, lecture=None):
    try:
        return reportService.createReport(kind, subject, lecture)
    except Exception as e:
        print("[CONTROLLER]Error creating report:", e)
        raise e
