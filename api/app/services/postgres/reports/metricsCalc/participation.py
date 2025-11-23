from app.services.postgres.reports.metricsCalc.utils import (
    is_active_participation,
    get_time_diff_minutes,
    is_lecture_tab
)


def calculate_camera_engagement(traces):
    """
    Calcula a % do tempo que os alunos passaram com câmera ativa
    vs tempo total de sessão
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)

        camera_engagements = []

        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue

            sorted_traces = sorted(
                user_traces, key=lambda x: x.get('timestamp', ''))

            total_camera_time = 0.0
            total_session_time = 0.0

            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]

                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'),
                    curr_trace.get('timestamp')
                )

                if time_diff > 0:
                    total_session_time += time_diff

                    # Se a câmera estava ativa no trace anterior, conta como tempo engajado
                    if prev_trace.get('cameraEnabled', False) or prev_trace.get('cameraStreaming', False):
                        total_camera_time += time_diff

            if total_session_time > 0:
                camera_engagement = total_camera_time / total_session_time
                camera_engagements.append(camera_engagement)
                print(
                    f"[CAMERA] Aluno {user}: {camera_engagement:.1%} câmera ativa ({total_camera_time:.1f}min / {total_session_time:.1f}min)")

        if not camera_engagements:
            return 0.0

        avg_camera_engagement = sum(
            camera_engagements) / len(camera_engagements)
        print(f"[SERVICE] camera_engagement: {avg_camera_engagement:.1%}")

        return round(avg_camera_engagement, 3)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular camera_engagement: {e}")
        return 0.0


def calculate_mic_engagement(traces):
    """
    Calcula a % do tempo que os alunos passaram com microfone ativo
    vs tempo total de sessão
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)

        mic_engagements = []

        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue

            sorted_traces = sorted(
                user_traces, key=lambda x: x.get('timestamp', ''))

            total_mic_time = 0.0
            total_session_time = 0.0

            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]

                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'),
                    curr_trace.get('timestamp')
                )

                if time_diff > 0:
                    total_session_time += time_diff

                    # Se o microfone estava ativo no trace anterior, conta como tempo engajado
                    if prev_trace.get('microphoneEnabled', False) or prev_trace.get('microphoneStreaming', False):
                        total_mic_time += time_diff

            if total_session_time > 0:
                mic_engagement = total_mic_time / total_session_time
                mic_engagements.append(mic_engagement)
                print(
                    f"[MIC] Aluno {user}: {mic_engagement:.1%} microfone ativo ({total_mic_time:.1f}min / {total_session_time:.1f}min)")

        if not mic_engagements:
            return 0.0

        avg_mic_engagement = sum(mic_engagements) / len(mic_engagements)
        print(f"[SERVICE] mic_engagement: {avg_mic_engagement:.1%}")

        return round(avg_mic_engagement, 3)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular mic_engagement: {e}")
        return 0.0


def calculate_voluntary_participation(traces):
    """
    Calcula a % da sessão onde o aluno estava participando ativamente
    (com câmera OU microfone ativo, E na aba da aula)
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)

        participation_ratios = []

        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue

            sorted_traces = sorted(
                user_traces, key=lambda x: x.get('timestamp', ''))

            total_participation_time = 0.0
            total_session_time = 0.0

            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]

                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'),
                    curr_trace.get('timestamp')
                )

                if time_diff > 0:
                    total_session_time += time_diff

                    # Considera participação voluntária quando:
                    # - Está na aba da aula E
                    # - Tem câmera ativa OU microfone ativo
                    if (is_lecture_tab(prev_trace) and
                        (prev_trace.get('cameraEnabled', False) or
                         prev_trace.get('microphoneEnabled', False) or
                         prev_trace.get('cameraStreaming', False) or
                         prev_trace.get('microphoneStreaming', False))):
                        total_participation_time += time_diff

            if total_session_time > 0:
                participation_ratio = total_participation_time / total_session_time
                participation_ratios.append(participation_ratio)
                print(
                    f"[PARTICIPATION] Aluno {user}: {participation_ratio:.1%} participação ativa ({total_participation_time:.1f}min / {total_session_time:.1f}min)")

        if not participation_ratios:
            return 0.0

        avg_participation = sum(participation_ratios) / \
            len(participation_ratios)
        print(f"[SERVICE] voluntary_participation: {avg_participation:.1%}")

        return round(avg_participation, 3)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular voluntary_participation: {e}")
        return 0.0
