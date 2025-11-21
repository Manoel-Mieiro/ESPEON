from datetime import datetime

def calculate_lecture_focus_ratio(traces):
    """
    Calcula a % do tempo que os alunos passaram com foco na aba da aula
    vs tempo total de sessão
    """
    try:
        # Agrupa traces por aluno
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)
        
        focus_ratios = []
        
        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue
                
            # Ordena por timestamp
            sorted_traces = sorted(user_traces, key=lambda x: x.get('timestamp', ''))
            
            total_focus_time = 0.0
            total_session_time = 0.0
            
            # Analisa cada intervalo entre traces
            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]
                
                # Calcula diferença de tempo entre traces
                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'), 
                    curr_trace.get('timestamp')
                )
                
                if time_diff > 0:
                    total_session_time += time_diff
                    
                    # Se estava na aba da aula no trace anterior, conta como foco
                    if is_lecture_tab(prev_trace):
                        total_focus_time += time_diff
            
            if total_session_time > 0:
                focus_ratio = total_focus_time / total_session_time
                focus_ratios.append(focus_ratio)
                print(f"[FOCUS] Aluno {user}: {focus_ratio:.1%} foco ({total_focus_time:.1f}min / {total_session_time:.1f}min)")
        
        if not focus_ratios:
            return 0.0
            
        avg_focus_ratio = sum(focus_ratios) / len(focus_ratios)
        print(f"[SERVICE] lecture_focus_ratio: {avg_focus_ratio:.1%}")
        
        return round(avg_focus_ratio, 3)
        
    except Exception as e:
        print(f"[SERVICE] Erro ao calcular lecture_focus_ratio: {e}")
        return 0.0
    
def calculate_focus_durations(traces):
    """
    Calcula tempo médio e máximo de foco contínuo na aula
    """
    try:
        student_sessions = {}
        for trace in traces:
            user = trace.get('user')
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(trace)
        
        all_focus_segments = []
        
        for user, user_traces in student_sessions.items():
            if len(user_traces) < 2:
                continue
                
            sorted_traces = sorted(user_traces, key=lambda x: x.get('timestamp', ''))
            
            current_focus_start = None
            current_focus_duration = 0.0
            
            for i in range(1, len(sorted_traces)):
                prev_trace = sorted_traces[i-1]
                curr_trace = sorted_traces[i]
                
                time_diff = get_time_diff_minutes(
                    prev_trace.get('timestamp'), 
                    curr_trace.get('timestamp')
                )
                
                # Se estava na aula no trace anterior
                if is_lecture_tab(prev_trace):
                    if current_focus_start is None:
                        # Inicia novo segmento de foco
                        current_focus_start = prev_trace.get('timestamp')
                    
                    current_focus_duration += time_diff
                else:
                    # Termina segmento de foco
                    if current_focus_duration > 0:
                        all_focus_segments.append(current_focus_duration)
                        current_focus_duration = 0.0
                        current_focus_start = None
            
            # Adiciona último segmento se existir
            if current_focus_duration > 0:
                all_focus_segments.append(current_focus_duration)
        
        if not all_focus_segments:
            return 0.0, 0.0
            
        avg_focus = sum(all_focus_segments) / len(all_focus_segments)
        max_focus = max(all_focus_segments)
        
        print(f"[SERVICE] avg_focus_duration: {avg_focus:.1f} minutos")
        print(f"[SERVICE] max_focus_duration: {max_focus:.1f} minutos")
        print(f"[SERVICE] Segmentos de foco analisados: {len(all_focus_segments)}")
        print(f"[SERVICE] Durações: {[f'{d:.1f}min' for d in sorted(all_focus_segments)]}")
        
        return round(avg_focus, 2), round(max_focus, 2)
        
    except Exception as e:
        print(f"[SERVICE] Erro ao calcular focus_durations: {e}")
        return 0.0, 0.0
    
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