from datetime import datetime


def is_lecture_tab(trace):
    """
    Verifica se o trace indica que o usuário estava na aba da aula
    """
    url = trace.get('url', '').lower()
    tab_state = trace.get('lectureTabState', '').lower()

    # Critérios para considerar "foco na aula":
    # 1. URL do Teams de reunião
    # 2. Tab state como 'active'
    # 3. Lecture audible como True
    teams_meeting = 'teams.microsoft.com' in url and '/l/meetup-join/' in url
    tab_active = tab_state == 'active'
    lecture_audible = trace.get('lectureAudible', False)

    return teams_meeting or tab_active or lecture_audible


def get_time_diff_minutes(time1_str, time2_str):
    """
    Calcula diferença em minutos entre dois timestamps no formato HH:MM:SS
    """
    try:
        if not time1_str or not time2_str:
            return 0.0

        time1 = datetime.strptime(time1_str, '%H:%M:%S')
        time2 = datetime.strptime(time2_str, '%H:%M:%S')

        # Se time2 for menor, assume que é do dia seguinte
        if time2 < time1:
            time2 = time2.replace(day=time2.day + 1)

        diff_seconds = (time2 - time1).total_seconds()
        return diff_seconds / 60.0  # converte para minutos

    except Exception as e:
        print(f"Erro ao calcular diferença de tempo: {e}")
        return 0.0


def is_active_participation(trace):
    """
    Verifica se o trace indica participação ativa na aula
    """
    # Está na aba da aula
    if not is_lecture_tab(trace):
        return False

    # E tem pelo menos um periférico ativo
    camera_active = trace.get('cameraEnabled', False) or trace.get(
        'cameraStreaming', False)
    mic_active = trace.get('microphoneEnabled', False) or trace.get(
        'microphoneStreaming', False)

    return camera_active or mic_active
