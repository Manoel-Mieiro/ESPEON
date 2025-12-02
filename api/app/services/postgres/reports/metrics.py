from datetime import datetime, timedelta

from flask import jsonify
from app.services.postgres.lectures import findOneLecture
import requests
import os


flask_port = os.getenv("FLASK_RUN_PORT", "8183")

def timeStrToEpochMs(time_str: str) -> float:
    """
    Converte string "HH:MM:SS" para epoch ms usando data dummy.
    """
    dt = datetime.strptime(time_str, "%H:%M:%S")
    dummy_date = datetime(2000, 1, 1, dt.hour, dt.minute, dt.second)
    return dummy_date.timestamp() * 1000  # ms

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

        lectures = findOneLecture(lecture_id)
        
        if not lectures or len(lectures) == 0:
            raise ValueError(f"Aula {lecture_id} não encontrada")
        
        lecture = lectures[0] if isinstance(lectures, list) else lectures

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

        print(
            f"[SERVICE] Lecture {lecture_id}: pct_enabled_camera={pct_camera}%, pct_enabled_mic={pct_mic}%")
        return pct_camera, pct_mic

    except Exception as e:
        print(
            f"[SERVICE] Erro ao calcular pct_camera/pct_mic para lecture_id={lecture_id}: {e}")
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
        print(
            f"[SERVICE] Calculando avg_idle_duration para lecture_id={lecture_id}")

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
            print(
                f"[SERVICE] Nenhum idle válido encontrado para {lecture_id}.")
            return 0.0

        avg_idle = sum(idle_durations) / len(idle_durations)
        print(
            f"[SERVICE] avg_idle_duration calculado: {avg_idle:.2f} minutos.")
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
        print(
            f"[SERVICE] Lecture {lecture_id}: avg_attention_span calculado = {avg_attention_span:.2f} minutos")
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

        durations = [(l['period_end'] - l['period_start']
                      ).total_seconds() / 60 for l in lectures]
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

