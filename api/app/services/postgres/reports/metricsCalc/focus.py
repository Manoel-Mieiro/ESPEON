from app.services.postgres.reports.metricsCalc.utils import (
    get_time_diff_minutes,
    is_lecture_tab
)

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
