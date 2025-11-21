from app.services.postgres.reports.metricsCalc.utils import (
    get_time_diff_minutes,
    is_lecture_tab
)


def calculate_distraction_ratio(traces):
    """
    Calcula a % do tempo que os alunos passaram em sites de distração
    vs tempo total de sessão
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)

        distraction_ratios = []

        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue

            sorted_traces = sorted(
                user_traces, key=lambda x: x.get('timestamp', ''))

            total_distraction_time = 0.0
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

                    # Se estava em distração no trace anterior, conta como tempo distraído
                    if is_distraction(prev_trace):
                        total_distraction_time += time_diff

            if total_session_time > 0:
                distraction_ratio = total_distraction_time / total_session_time
                distraction_ratios.append(distraction_ratio)
                print(
                    f"[DISTRACTION] Aluno {user}: {distraction_ratio:.1%} distraído ({total_distraction_time:.1f}min / {total_session_time:.1f}min)")

        if not distraction_ratios:
            return 0.0

        avg_distraction_ratio = sum(
            distraction_ratios) / len(distraction_ratios)
        print(f"[SERVICE] distraction_ratio: {avg_distraction_ratio:.1%}")

        return round(avg_distraction_ratio, 3)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular distraction_ratio: {e}")
        return 0.0


def calculate_distraction_frequency(traces):
    """
    Calcula quantas vezes por hora os alunos trocam para distrações
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)

        distraction_frequencies = []

        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue

            sorted_traces = sorted(
                user_traces, key=lambda x: x.get('timestamp', ''))

            distraction_switches = 0
            total_session_time = 0.0
            was_in_lecture = is_lecture_tab(sorted_traces[0])

            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]

                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'),
                    curr_trace.get('timestamp')
                )
                total_session_time += time_diff

                # Detecta transição: estava na aula e agora foi para distração
                prev_in_lecture = is_lecture_tab(prev_trace)
                curr_in_distraction = is_distraction(curr_trace)

                if prev_in_lecture and curr_in_distraction:
                    distraction_switches += 1

            # Calcula frequência por hora
            if total_session_time > 0:
                frequency_per_hour = (
                    distraction_switches / total_session_time) * 60
                distraction_frequencies.append(frequency_per_hour)
                print(
                    f"[DISTRACTION] Aluno {user}: {frequency_per_hour:.1f} distrações/hora ({distraction_switches} switches em {total_session_time:.1f}min)")

        if not distraction_frequencies:
            return 0.0

        avg_frequency = sum(distraction_frequencies) / \
            len(distraction_frequencies)
        print(f"[SERVICE] distraction_frequency: {avg_frequency:.1f}/hora")

        return round(avg_frequency, 1)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular distraction_frequency: {e}")
        return 0.0


def calculate_main_distractions(traces):
    """
    Identifica os principais sites de distração e calcula a % do tempo em cada
    """
    try:
        distraction_categories = {
            'chatgpt': 0.0,
            'github': 0.0,
            'extensions': 0.0,
            'social': 0.0,
            'email': 0.0,
            'docs': 0.0,
            'other': 0.0
        }

        total_distraction_time = 0.0

        for i in range(1, len(traces)):
            prev_trace = traces[i-1]
            curr_trace = traces[i]

            time_diff = get_time_diff_minutes(
                prev_trace.get('timestamp'),
                curr_trace.get('timestamp')
            )

            if time_diff > 0 and is_distraction(prev_trace):
                total_distraction_time += time_diff

                # Classifica o tipo de distração
                distraction_type = classify_distraction(prev_trace)
                distraction_categories[distraction_type] += time_diff

        # Calcula porcentagens
        if total_distraction_time > 0:
            main_distractions = {}
            for category, time in distraction_categories.items():
                if time > 0:
                    percentage = time / total_distraction_time
                    main_distractions[category] = round(percentage, 3)

            # Ordena por porcentagem (maior primeiro)
            main_distractions = dict(sorted(
                main_distractions.items(),
                key=lambda x: x[1],
                reverse=True
            ))

            print(f"[SERVICE] main_distractions: {main_distractions}")
            return main_distractions

        return {'other': 1.0}  # fallback

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular main_distractions: {e}")
        return {'other': 1.0}


def is_distraction(trace):
    """
    Verifica se o trace indica uma distração
    """
    if is_lecture_tab(trace):
        return False

    url = trace.get('url', '').lower()
    title = trace.get('title', '').lower()

    # Lista de distrações conhecidas
    distractions = [
        'chatgpt.com', 'openai.com',
        'github.com', 'gitlab.com',
        'edge://extensions', 'chrome://extensions',
        'facebook.com', 'instagram.com', 'twitter.com', 'x.com', 'tiktok.com',
        'gmail.com', 'outlook.com', 'yahoo.com',
        'youtube.com', 'netflix.com', 'twitch.tv',
        'reddit.com', 'linkedin.com'
    ]

    return any(distraction in url for distraction in distractions)


def classify_distraction(trace):
    """
    Classifica o tipo de distração
    """
    url = trace.get('url', '').lower()
    title = trace.get('title', '').lower()

    if 'chatgpt.com' in url or 'openai.com' in url:
        return 'chatgpt'
    elif 'github.com' in url or 'gitlab.com' in url:
        return 'github'
    elif 'edge://extensions' in url or 'chrome://extensions' in url:
        return 'extensions'
    elif any(social in url for social in ['facebook.com', 'instagram.com', 'twitter.com', 'x.com', 'tiktok.com']):
        return 'social'
    elif any(email in url for email in ['gmail.com', 'outlook.com', 'yahoo.com']):
        return 'email'
    elif any(doc in url for doc in ['docs.google.com', 'notion.so', 'drive.google.com']):
        return 'docs'
    else:
        return 'other'
