import app.repository.postgres.reportsRepository as reports
import requests
import os


"""
GLOBALS
"""
flask_port = os.getenv("FLASK_RUN_PORT", "8183")



"""
CRUDS
"""
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
        report = populateReportMetrics(report)
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


def populateReportMetrics(report: object):
    """
    Calcula e preenche campos derivados do relatório (ex: total_students, tempo médio, etc.)
    """ 
    total_students = calculateTotalStudents(report._lecture_id)
    report._total_students = total_students
    return report



"""
Campos do Relatório
"""


def calculateTotalStudents(lecture_id: str):
    """
    Retorna o número de estudantes únicos que participaram de uma aula (lecture_id).
    Faz uma chamada à API de traces e conta os usuários distintos.
    """
    try:
        base_url = f"http://localhost:{flask_port}/traces/?id={lecture_id}"

        response = requests.get(base_url)
        response.raise_for_status()

        traces = response.json()

        unique_users = {trace.get("user")
                        for trace in traces if trace.get("user")}
        total_students = len(unique_users)

        print(
            f"[SERVICE] Lecture {lecture_id} tem {total_students} estudantes únicos.")
        return total_students

    except Exception as e:
        print(
            f"[SERVICE] Erro ao calcular total de estudantes para {lecture_id}: {e}")
        raise e

def calculateTotalTimeWatched(lecture_id: str):
    """
    Calcula o tempo total assistido (em minutos) com base na duração da aula (lecture).
    Usa period_start e period_end da tabela lecture.
    """
    try:
        print(f"[SERVICE] Calculando total_time_watched para lecture_id={lecture_id}")

        lecture = lectures.getLectureById(lecture_id) 

        base_url = f"http://localhost:{flask_port}/lectures/?id={lecture_id}"

        response = requests.get(base_url)
        response.raise_for_status()

        traces = response.json()

        if not lecture:
            raise ValueError(f"Aula {lecture_id} não encontrada no banco de dados.")

        period_start = lecture.period_start
        period_end = lecture.period_end

        if not period_start or not period_end:
            raise ValueError(f"Aula {lecture_id} possui campos nulos em period_start/period_end.")

        duration = (period_end - period_start).total_seconds() / 60  # minutos
        print(f"[SERVICE] Duração calculada: {duration:.2f} minutos.")

        return round(duration, 2)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular total_time_watched: {e}")
        raise e