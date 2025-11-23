from app.services.postgres.reports.metricsCalc.utils import (
    get_time_diff_minutes,
    is_lecture_tab
)

from app.services.postgres.reports.metricsCalc.disturb import (
    is_distraction
)


def calculate_tab_switch_frequency(traces):
    """
    Calcula quantas vezes por hora os alunos trocam de aba (qualquer aba)
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)

        switch_frequencies = []

        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue

            sorted_traces = sorted(
                user_traces, key=lambda x: x.get('timestamp', ''))

            total_switches = 0
            total_session_time = 0.0
            last_url = sorted_traces[0].get('url', '')

            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]

                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'),
                    curr_trace.get('timestamp')
                )
                total_session_time += time_diff

                # Detecta troca de aba (mudança de URL)
                current_url = curr_trace.get('url', '')
                if current_url != last_url:
                    total_switches += 1
                    last_url = current_url

            # Calcula frequência por hora
            if total_session_time > 0:
                frequency_per_hour = (total_switches / total_session_time) * 60
                switch_frequencies.append(frequency_per_hour)
                print(
                    f"[TAB_SWITCH] Aluno {user}: {frequency_per_hour:.1f} trocas/hora ({total_switches} switches em {total_session_time:.1f}min)")

        if not switch_frequencies:
            return 0.0

        avg_frequency = sum(switch_frequencies) / len(switch_frequencies)
        print(f"[SERVICE] tab_switch_frequency: {avg_frequency:.1f}/hora")

        return round(avg_frequency, 1)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular tab_switch_frequency: {e}")
        return 0.0


def calculate_multitasking_intensity(traces):
    """
    Calcula uma escala 0-1 que representa a intensidade de multitasking
    Baseado na relação entre tempo focado vs tempo distraído e frequência de switches
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)

        multitasking_scores = []

        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue

            sorted_traces = sorted(
                user_traces, key=lambda x: x.get('timestamp', ''))

            total_session_time = 0.0
            focus_to_distraction_switches = 0
            total_switches = 0
            last_was_focus = is_lecture_tab(sorted_traces[0])
            last_url = sorted_traces[0].get('url', '')

            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]

                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'),
                    curr_trace.get('timestamp')
                )
                total_session_time += time_diff

                # Detecta qualquer troca de aba
                current_url = curr_trace.get('url', '')
                if current_url != last_url:
                    total_switches += 1

                    # Detecta troca específica: foco → distração
                    if last_was_focus and is_distraction(curr_trace):
                        focus_to_distraction_switches += 1

                    last_url = current_url
                    last_was_focus = is_lecture_tab(curr_trace)

            # Calcula score de multitasking (0-1)
            if total_switches > 0 and total_session_time > 0:
                # Fator 1: Proporção de switches que são foco→distração
                distraction_switch_ratio = focus_to_distraction_switches / total_switches

                # Fator 2: Frequência geral de switches (normalizada)
                switch_frequency = (
                    total_switches / total_session_time) * 60  # por hora
                # assume 30/hora como máximo
                normalized_frequency = min(switch_frequency / 30.0, 1.0)

                # Score final: média dos dois fatores
                multitasking_score = (
                    distraction_switch_ratio + normalized_frequency) / 2
                multitasking_scores.append(multitasking_score)

                print(
                    f"[MULTITASKING] Aluno {user}: intensidade {multitasking_score:.2f} (switches: {distraction_switch_ratio:.1%} foco→distração, {switch_frequency:.1f}/hora)")

        if not multitasking_scores:
            return 0.0

        avg_multitasking = sum(multitasking_scores) / len(multitasking_scores)
        print(f"[SERVICE] multitasking_intensity: {avg_multitasking:.2f}")

        return round(avg_multitasking, 2)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular multitasking_intensity: {e}")
        return 0.0


def calculate_focus_fragmentation(traces):
    """
    Calcula quantos segmentos de foco por hora os alunos têm
    (indica quão fragmentada é a atenção)
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)

        fragmentation_rates = []

        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue

            sorted_traces = sorted(
                user_traces, key=lambda x: x.get('timestamp', ''))

            total_focus_segments = 0
            total_session_time = 0.0
            in_focus_segment = False

            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]

                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'),
                    curr_trace.get('timestamp')
                )
                total_session_time += time_diff

                # Detecta início de segmento de foco
                if is_lecture_tab(prev_trace) and not in_focus_segment:
                    total_focus_segments += 1
                    in_focus_segment = True

                # Detecta fim de segmento de foco
                if not is_lecture_tab(prev_trace) and in_focus_segment:
                    in_focus_segment = False

            # Calcula taxa de fragmentação (segmentos por hora)
            if total_session_time > 0:
                fragmentation_rate = (
                    total_focus_segments / total_session_time) * 60
                fragmentation_rates.append(fragmentation_rate)
                print(
                    f"[FRAGMENTATION] Aluno {user}: {fragmentation_rate:.1f} segmentos/hora ({total_focus_segments} segmentos em {total_session_time:.1f}min)")

        if not fragmentation_rates:
            return 0.0

        avg_fragmentation = sum(fragmentation_rates) / len(fragmentation_rates)
        print(f"[SERVICE] focus_fragmentation: {avg_fragmentation:.1f}/hora")

        return round(avg_fragmentation, 1)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular focus_fragmentation: {e}")
        return 0.0
