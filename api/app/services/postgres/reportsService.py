import app.repository.postgres.reportsRepository as reports
from datetime import datetime, timedelta
import requests
import os


"""
GLOBALS
"""
flask_port = os.getenv("FLASK_RUN_PORT", "8183")


def timeStrToEpochMs(time_str: str) -> float:
    """
    Converte string "HH:MM:SS" para epoch ms usando data dummy.
    """
    dt = datetime.strptime(time_str, "%H:%M:%S")
    dummy_date = datetime(2000, 1, 1, dt.hour, dt.minute, dt.second)
    return dummy_date.timestamp() * 1000  # ms


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
    pct_enabled_camera, pct_enabled_mic = calculateCameraMicUsage(
        report._lecture_id)
    avg_idle_duration = calculateAvgIdle(report._lecture_id)

    report._total_students = total_students
    report._total_time_watched = total_time_watched
    report._avg_lecture_duration = avg_lecture_duration
    report._pct_enabled_camera = pct_enabled_camera
    report._pct_enabled_mic = pct_enabled_mic
    report._avg_idle_duration = avg_idle_duration
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


def calculateAvgLectureDuration(subject_id: str) -> float:
    """
    Calcula a duração média de todas as aulas de uma disciplina (subject_id)
    Retorna em minutos (float)
    """
    try:
        print(
            f"[SERVICE] Calculando avgLectureDuration para subject_id={subject_id}")

        response = requests.get(
            f"http://localhost:8183/lectures/subject/{subject_id}"
        ).json()

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
                # Converte para epoch ms
                start_ms = timeStrToEpochMs(period_start)
                end_ms = timeStrToEpochMs(period_end)

                # Ajuste se aula passar da meia-noite
                if end_ms < start_ms:
                    end_ms += 24 * 60 * 60 * 1000  # +1 dia em ms

                duration_min = (end_ms - start_ms) / (1000 * 60)
                total_minutes += duration_min
                count += 1
            else:
                print(
                    f"[SERVICE] Aula {lecture.get('lecture_id')} com period_start/period_end nulos, ignorando")

        avgLectureDuration = total_minutes / count if count > 0 else 0.0
        print(
            f"[SERVICE] Duração média calculada: {avgLectureDuration:.2f} minutos para subject_id={subject_id}")
        return round(avgLectureDuration, 2)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular avgLectureDuration: {e}")
        raise e


def calculateCameraMicUsage(lecture_id: str):
    """
    Calcula o percentual de câmeras e microfones ligados durante a aula.
    Usa a API de traces.
    Retorna (pct_camera, pct_mic) em float (%)
    """
    try:
        url = f"http://localhost:{flask_port}/traces/{lecture_id}"
        response = requests.get(url)
        response.raise_for_status()

        traces = response.json()
        if not traces:
            print(
                f"[SERVICE] Nenhum trace encontrado para lecture_id={lecture_id}")
            return 0.0, 0.0

        total = len(traces)
        camera_on = sum(1 for t in traces if t.get("cameraEnabled") is True)
        mic_on = sum(1 for t in traces if t.get("microphoneEnabled") is True)

        pct_camera = round(camera_on / total * 100, 2)
        pct_mic = round(mic_on / total * 100, 2)

        print(
            f"[SERVICE] Lecture {lecture_id}: pct_enabled_camera={pct_camera}%, pct_enabled_mic={pct_mic}%"
        )
        return pct_camera, pct_mic

    except Exception as e:
        print(
            f"[SERVICE] Erro ao calcular pct_camera/pct_mic para lecture_id={lecture_id}: {e}")
        return 0.0, 0.0


def calculateAvgIdle(lecture_id: str) -> float:
    """
    Calcula a média de tempo ocioso (idle) dos alunos em uma aula.
    idle_duration = timestamp - lectureTabLastAccessed (em minutos)
    """
    try:
        print(
            f"[SERVICE] Calculando avg_idle_duration para lecture_id={lecture_id}")

        base_url = f"http://localhost:{flask_port}/traces/{lecture_id}"
        response = requests.get(base_url)
        response.raise_for_status()

        traces = response.json()
        if not traces:
            raise ValueError(
                f"Nenhum trace encontrado para a aula {lecture_id}.")

        idle_durations = []
        for trace in traces:
            ts_str = trace.get("timestamp")
            last_access_str = trace.get("lectureTabLastAccessed")

            if ts_str is None or last_access_str is None:
                continue

            ts_ms = timeStrToEpochMs(ts_str)
            last_access_ms = timeStrToEpochMs(last_access_str)

            # Calcular idle duration em minutos
            idle_min = (last_access_ms - ts_ms) / (1000 * 60)
            if idle_min >= 0:
                idle_durations.append(idle_min)

        if not idle_durations:
            print(
                f"[SERVICE] Nenhum idle válido encontrado para {lecture_id}.")
            return 0.0

        avg_idle = sum(idle_durations) / len(idle_durations)
        print(
            f"[SERVICE] avg_idle_duration calculado: {avg_idle:.2f} minutos.")

        return round(avg_idle, 2)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular avg_idle_duration: {e}")
        raise e
