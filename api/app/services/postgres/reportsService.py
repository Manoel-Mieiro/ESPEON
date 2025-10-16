import app.repository.postgres.reportsRepository as reports
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import requests
import os


"""
GLOBALS
"""
flask_port = os.getenv("FLASK_RUN_PORT", "8183")


def fetchLectureTraces(lecture_id: str):
    """
    Busca os traces de uma aula e retorna o JSON diretamente.

    Args:
        lecture_id (str): ID da aula

    Returns:
        list: lista de traces da aula
    """
    try:
        flask_port = os.getenv("FLASK_RUN_PORT", "8183")
        base_url = f"http://localhost:{flask_port}/traces/{lecture_id}"
        response = requests.get(base_url)
        response.raise_for_status()
        traces = response.json()
        return traces

    except Exception as e:
        print(
            f"[SERVICE] Erro ao buscar traces para lecture_id={lecture_id}: {e}")
        return []


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

    traces = fetchLectureTraces(report._lecture_id)

    # Calcula métricas usando os traces
    total_students = calculateTotalStudents(traces)
    total_time_watched = calculateTotalTimeWatched(report._lecture_id)
    avg_lecture_duration = calculateAvgLectureDuration(report._subject_id)
    pct_enabled_camera, pct_enabled_mic = calculateCameraMicUsage(traces)
    avg_idle_duration = calculateAvgIdle(traces)
    avg_attention_span = calculateAvgAttentionSpan(traces, total_time_watched, total_students, avg_idle_duration)
    min_idle_duration, max_idle_duration = getIdleMinMax(traces)
    min_attention_span, max_attention_span = getAttentionSpanMinMax(traces, total_time_watched, total_students)


    # Atualiza o objeto report
    report._total_students = total_students
    report._total_time_watched = total_time_watched
    report._avg_lecture_duration = avg_lecture_duration
    report._pct_enabled_camera = pct_enabled_camera
    report._pct_enabled_mic = pct_enabled_mic
    report._avg_idle_duration = avg_idle_duration
    report._avg_attention_span = avg_attention_span
    report._min_idle_duration = min_idle_duration
    report._max_idle_duration = max_idle_duration
    report._min_attention_span = min_attention_span
    report._max_attention_span = max_attention_span

    return report



"""
Campos do Relatório
"""

def calculateTotalStudents(traces):
    """
    Retorna o número de estudantes únicos que participaram de uma aula (lecture_id).
    Faz uma chamada à API de traces e conta os usuários distintos.
    """
    try:

        unique_users = {trace.get("user")
                        for trace in traces if trace.get("user")}
        total_students = len(unique_users)

        lecture_id = traces[0].get("lecture_id") if traces else "desconhecido"
        print(
            f"[SERVICE] Lecture {lecture_id} tem {total_students} estudantes únicos.")
        return total_students

    except Exception as e:
        print(
            f"[SERVICE] Erro ao calcular total de estudantes para {traces.get("lecture_id")}: {e}")
        raise e


def calculateTotalTimeWatched(lecture_id):
    """
    Calcula o tempo total assistido (em minutos) com base na duração da aula (lecture).
    """
    try:
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


def calculateCameraMicUsage(traces):
    """
    Calcula o percentual de câmeras e microfones ligados durante a aula.
    Usa a API de traces.
    Retorna (pct_camera, pct_mic) em float (%)
    """
    try:
        if not traces:
            print(f"[SERVICE] Nenhum trace encontrado.")
            return 0.0, 0.0

        lecture_id = traces[0].get("lecture_id") if traces else "desconhecido"

        total = len(traces)
        camera_on = sum(1 for t in traces if t.get("cameraEnabled") is True)
        mic_on = sum(1 for t in traces if t.get("microphoneEnabled") is True)

        pct_camera = round(camera_on / total * 100, 2)
        pct_mic = round(mic_on / total * 100, 2)

        print(f"[SERVICE] Lecture {lecture_id}: pct_enabled_camera={pct_camera}%, pct_enabled_mic={pct_mic}%")
        return pct_camera, pct_mic

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular pct_camera/pct_mic para lecture_id={lecture_id}: {e}")
        return 0.0, 0.0



def calculateAvgIdle(traces) -> float:
    """
    Calcula a média de tempo ocioso (idle) dos alunos em uma aula.
    idle_duration = lectureTabLastAccessed - timestamp (em minutos)

    Args:
        traces (list): lista de dicionários com os traces da aula

    Returns:
        float: tempo médio ocioso por aluno (em minutos), arredondado para 2 casas decimais
    """
    try:
        if not traces:
            print(f"[SERVICE] Nenhum trace encontrado.")
            return 0.0

        lecture_id = traces[0].get("lecture_id") if traces else "desconhecido"
        print(f"[SERVICE] Calculando avg_idle_duration para lecture_id={lecture_id}")

        idle_durations = []
        for trace in traces:
            ts_str = trace.get("timestamp")
            last_access_str = trace.get("lectureTabLastAccessed")
            if not ts_str or not last_access_str:
                continue

            # converte para epoch ms 
            ts_ms = timeStrToEpochMs(ts_str)
            last_access_ms = timeStrToEpochMs(last_access_str)

            # idle duration em minutos
            idle_min = (last_access_ms - ts_ms) / (1000 * 60)
            if idle_min >= 0:
                idle_durations.append(idle_min)

        if not idle_durations:
            print(f"[SERVICE] Nenhum idle válido encontrado para {lecture_id}.")
            return 0.0

        avg_idle = sum(idle_durations) / len(idle_durations)
        print(f"[SERVICE] avg_idle_duration calculado: {avg_idle:.2f} minutos.")
        return round(avg_idle, 2)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular avg_idle_duration: {e}")
        return 0.0


def calculateAvgAttentionSpan(traces, total_time_watched: float, total_students: int, avg_idle_duration: float) -> float:
    """
    Calcula o tempo médio de atenção (avg_attention_span) dos alunos em uma aula.

    Fórmula:
        avg_attention_span = avg_watch_duration - avg_idle_duration

    Onde:
        avg_watch_duration = total_time_watched / total_students

    Args:
        traces (list): lista de dicionários com os traces da aula
        total_time_watched (float): tempo total assistido por todos os alunos (em minutos)
        total_students (int): quantidade de alunos na aula

    Returns:
        float: tempo médio de atenção por aluno (em minutos), arredondado para 2 casas decimais
    """
    try:
        if total_students <= 0:
            print("[SERVICE] total_students é zero ou negativo, retornando 0.0")
            return 0.0

        avg_watch_duration = total_time_watched / total_students

        avg_attention_span = avg_watch_duration - avg_idle_duration

        avg_attention_span = max(avg_attention_span, 0.0)

        lecture_id = traces[0].get("lecture_id") if traces else "desconhecido"
        print(f"[SERVICE] Lecture {lecture_id}: avg_attention_span calculado = {avg_attention_span:.2f} minutos")
        return round(avg_attention_span, 2)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular avg_attention_span: {e}")
        return 0.0

def getAvgLectureDurationMinMax(lectures):
    """
    Recebe uma lista de aulas (cada aula com period_start e period_end) e retorna
    (min_duration, max_duration) em minutos.
    """
    try:
        if not lectures:
            return 0.0, 0.0
        
        durations = [(l['period_end'] - l['period_start']).total_seconds() / 60 for l in lectures]
        return round(min(durations), 2), round(max(durations), 2)
    
    except Exception as e:
        print(f"[SERVICE] Erro em getAvgLectureDurationMinMax: {e}")
        return 0.0, 0.0

def getIdleMinMax(traces):
    """
    Recebe uma lista de traces e retorna (min_idle, max_idle) em minutos.
    """
    try:
        if not traces:
            return 0.0, 0.0

        idle_durations = []
        for trace in traces:
            ts_str = trace.get("timestamp")
            last_access_str = trace.get("lectureTabLastAccessed")
            if not ts_str or not last_access_str:
                continue
            ts_ms = timeStrToEpochMs(ts_str)
            last_access_ms = timeStrToEpochMs(last_access_str)
            idle_min = (last_access_ms - ts_ms) / (1000 * 60)
            if idle_min >= 0:
                idle_durations.append(idle_min)
        
        if not idle_durations:
            return 0.0, 0.0

        return round(min(idle_durations), 2), round(max(idle_durations), 2)

    except Exception as e:
        print(f"[SERVICE] Erro em getAvgIdleMinMax: {e}")
        return 0.0, 0.0

def getAttentionSpanMinMax(traces, total_time_watched, total_students):
    """
    Recebe traces, total_time_watched e total_students e retorna
    (min_attention, max_attention) em minutos.
    """
    try:
        if total_students <= 0 or not traces:
            return 0.0, 0.0

        avg_idle_duration = calculateAvgIdle(traces)
        avg_watch_duration = total_time_watched / total_students
        attention = avg_watch_duration - avg_idle_duration
        attention = max(attention, 0.0)

        return round(attention, 2), round(attention, 2)

    except Exception as e:
        print(f"[SERVICE] Erro em getAvgAttentionSpanMinMax: {e}")
        return 0.0, 0.0

def generateReportPdf(report):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, f"Relatório da Aula #{report._lecture_id}")

    # Informações gerais
    c.setFont("Helvetica", 12)
    y = height - 3.5 * cm
    line_height = 0.9 * cm

    c.drawString(2 * cm, y, f"Disciplina ID: {report._subject_id}"); y -= line_height
    c.drawString(2 * cm, y, f"Total de alunos: {report._total_students}"); y -= line_height
    c.drawString(2 * cm, y, f"Tempo total assistido: {report._total_time_watched or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Média de duração da aula: {report._avg_lecture_duration or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Duração ociosa média: {report._avg_idle_duration or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Atividade média (atenção): {report._avg_attention_span or 0:.0f} min"); y -= line_height

    # Seção de recursos
    c.setFont("Helvetica-Bold", 14)
    y -= 0.5 * cm
    c.drawString(2 * cm, y, "PERIFÉRICOS"); y -= line_height

    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, y, f"% tempo com câmera ligada: {report._pct_enabled_camera or 0:.0f}%"); y -= line_height
    c.drawString(2 * cm, y, f"% tempo com microfone ligado: {report._pct_enabled_mic or 0:.0f}%"); y -= line_height
    c.drawString(2 * cm, y, f"Média de streaming de câmera: {report._avg_cam_streaming_span or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Média de streaming de microfone: {report._avg_mic_streaming_span or 0:.0f} min"); y -= line_height

    # Estatísticas gerais
    c.setFont("Helvetica-Bold", 14)
    y -= 0.5 * cm
    c.drawString(2 * cm, y, "PICOS E DECLIVES"); y -= line_height

    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, y, f"Mín. duração da aula: {report._min_lecture_duration or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Máx. duração da aula: {report._max_lecture_duration or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Mín. tempo ocioso: {report._min_idle_duration or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Máx. tempo ocioso: {report._max_idle_duration or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Mín. atenção: {report._min_attention_span or 0:.0f} min"); y -= line_height
    c.drawString(2 * cm, y, f"Máx. atenção: {report._max_attention_span or 0:.0f} min"); y -= line_height

    # Rodapé
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(2 * cm, 2 * cm, f"Emitido em: {report._issued_at.strftime('%d/%m/%Y %H:%M')}")


    c.showPage()
    c.save()
    buffer.seek(0)

    return buffer