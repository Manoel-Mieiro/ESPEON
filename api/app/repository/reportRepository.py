from bson import ObjectId
from db import client
from app.models.reports import Reports

db = client["REPORTS"]


def findAllReports(kind):
    reports = db[kind]
    try:
        docs = list(reports.find({}))
        report_list = []

        for doc in docs:
            report = Reports.from_dict(doc)
            report_list.append(report.to_dict())

        return report_list

    except Exception as e:
        print("[REPOSITORY]Erro ao buscar reports:", e)
        raise e


def createReport(data: Reports, kind):
    reports = db[kind]
    try:
        print("\n[REPOSITORY]Criando report:", data, "\n")
        reportInstance = Reports(**data)
        result = reports.insert_one(reportInstance.to_dict())
        reportInstance._id = result.inserted_id

        if not reportInstance._id:
            raise Exception("Erro ao inserir report no banco.")

        return reportInstance.to_dict()
    except Exception as e:
        print("[REPOSITORY]Erro ao criar report:", e)
        raise e
