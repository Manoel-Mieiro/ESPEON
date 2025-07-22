import app.repository.reportRepository as repository
from app.services.reports.metrics import builReport

collection = None


def findAllReports(kind):
    try:
        return repository.findAllReports(kind)
    except Exception as e:
        print("[SERVICE]Erro ao buscar reports:", e)
        raise e


def createReport(kind, subject=None, lecture=None):
    try:
        print(f"Subject = {subject}")
        print(f"Lecture = {lecture}")
        print(f"[SERVICE]Criando report para. \nRelatório de {kind}")
        report = builReport(subject, lecture)
        return repository.createReport(report, kind)
    except Exception as e:
        print("[SERVICE]Erro ao criar report:", e)
        raise e


def extractSubject(subject):
    end = subject.index(']')
    substring = subject[1:end]
    return substring.lower().replace(" ", '_')
