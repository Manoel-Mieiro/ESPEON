import app.repository.postgres.reportsRepository as reports
from datetime import datetime, timedelta
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
    total_time_watched = calculateTotalTimeWatched(report._lecture_id)
    avg_lecture_duration = calculateAvgLectureDuration(report._subject_id)

    report._total_students = total_students
    report._total_time_watched = total_time_watched
    report._avg_lecture_duration = avg_lecture_duration
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
    """
    try:
        flask_port = os.getenv("FLASK_RUN_PORT", "8183")
        print(
            f"[SERVICE] Calculando total_time_watched para lecture_id={lecture_id}")

        base_url = f"http://localhost:{flask_port}/lectures/{lecture_id}"
        response = requests.get(base_url)
        response.raise_for_status()

        lecture = response.json()

        if not lecture:
            raise ValueError(f"Aula {lecture_id} não encontrada.")

        period_start = lecture.get("period_start")
        period_end = lecture.get("period_end")

        if not period_start or not period_end:
            raise ValueError(
                f"Aula {lecture_id} possui campos nulos em period_start/period_end.")

        # Converter strings para objetos time se necessário (considerando segundos)
        if isinstance(period_start, str):
            period_start = datetime.strptime(period_start, "%H:%M:%S").time()
        if isinstance(period_end, str):
            period_end = datetime.strptime(period_end, "%H:%M:%S").time()

        # Combinar com uma data dummy para calcular a diferença
        dummy_date = datetime(2000, 1, 1)
        start_dt = datetime.combine(dummy_date, period_start)
        end_dt = datetime.combine(dummy_date, period_end)

        # Ajuste se a aula terminar depois da meia-noite
        if end_dt < start_dt:
            end_dt = end_dt.replace(day=end_dt.day + 1)

        duration_minutes = (end_dt - start_dt).total_seconds() / 60
        print(f"[SERVICE] Duração calculada: {duration_minutes:.2f} minutos.")

        return round(duration_minutes, 2)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular total_time_watched: {e}")
        raise e


def calculateAvgLectureDuration(subject_id: str):
    """
    Calcula a duração média de todas as aulas de uma disciplina (subject_id)
    Retorna em minutos (float)
    """
    try:
        print(
            f"[SERVICE] Calculando avg_lecture_duration para subject_id={subject_id}")

        response = requests.get(
            f"http://localhost:8183/lectures/subject/{subject_id}").json()

        if not response:
            print(
                f"[SERVICE] Nenhuma aula encontrada para subject_id={subject_id}")
            return 0.0

        total_minutes = 0
        count = 0

        for lecture in response:
            period_start = lecture.get("period_start")
            period_end = lecture.get("period_end")

            if period_start and period_end:
                
                fmt = "%H:%M:%S"
                start_time = datetime.strptime(period_start, fmt).time()
                end_time = datetime.strptime(period_end, fmt).time()

                # Combina com data dummy
                dummy_date = datetime(2000, 1, 1)
                start_dt = datetime.combine(dummy_date, start_time)
                end_dt = datetime.combine(dummy_date, end_time)

                # Ajuste se aula passar da meia-noite
                if end_dt < start_dt:
                    end_dt += timedelta(days=1)

                duration = (end_dt - start_dt).total_seconds() / 60
                total_minutes += duration
                count += 1
            else:
                print(
                    f"[SERVICE] Aula {lecture.get('lecture_id')} com period_start/period_end nulos, ignorando")

        avg_duration = total_minutes / count if count > 0 else 0.0
        print(
            f"[SERVICE] Duração média calculada: {avg_duration:.2f} minutos para subject_id={subject_id}")
        return round(avg_duration, 2)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular avg_lecture_duration: {e}")
        raise e
