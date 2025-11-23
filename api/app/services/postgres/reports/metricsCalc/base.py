from datetime import datetime
from app.services.postgres.reports.metrics import calculateTotalTimeWatched

def calculate_real_avg_session_per_student(traces):
    """
    Calcula o tempo REAL médio que cada aluno ficou ativo na aula
    Baseado nos timestamps dos traces
    """
    try:
        student_sessions = {}
        
        # Agrupa traces por aluno
        for trace in traces:
            user = trace.get('user')
            timestamp = trace.get('timestamp')
            
            if user not in student_sessions:
                student_sessions[user] = []
            
            student_sessions[user].append(timestamp)
        
        session_durations = []
        
        for user, timestamps in student_sessions.items():
            if len(timestamps) < 2:
                # Se só tem um registro, considera tempo mínimo (ex: 1 minuto)
                session_durations.append(1.0)
                continue
                
            try:
                # Converte e ordena timestamps
                time_objects = [datetime.strptime(ts, '%H:%M:%S') for ts in timestamps]
                time_objects.sort()
                
                # Tempo ativo = diferença entre primeiro e último registro
                active_duration = (time_objects[-1] - time_objects[0]).total_seconds() / 60
                
                # Garante que pelo menos 1 minuto
                active_duration = max(active_duration, 1.0)
                session_durations.append(active_duration)
                
                print(f"[SESSION] Aluno {user}: {active_duration:.1f} minutos ativo")
                
            except Exception as e:
                print(f"Erro ao processar aluno {user}: {e}")
                session_durations.append(1.0)  # tempo mínimo
                continue
        
        if not session_durations:
            return 0.0
        
        avg_real_session = sum(session_durations) / len(session_durations)
        
        print(f"[SERVICE] avg_real_session_per_student: {avg_real_session:.2f} minutos")
        print(f"[SERVICE] Alunos analisados: {len(session_durations)}")
        print(f"[SERVICE] Tempos reais: {[f'{d:.1f}min' for d in session_durations]}")
        
        return round(avg_real_session, 2)
        
    except Exception as e:
        print(f"[SERVICE] Erro ao calcular tempo real médio: {e}")
        return 0.0
    
def calculate_real_total_session_duration(traces):
    """
    Calcula a soma total de tempo que todos os alunos ficaram ativos
    """
    try:
        student_sessions = {}
        
        for trace in traces:
            user = trace.get('user')
            timestamp = trace.get('timestamp')
            
            if user not in student_sessions:
                student_sessions[user] = []
            student_sessions[user].append(timestamp)
        
        total_duration = 0.0
        
        for user, timestamps in student_sessions.items():
            if len(timestamps) < 2:
                total_duration += 1.0  # tempo mínimo
                continue
                
            try:
                time_objects = [datetime.strptime(ts, '%H:%M:%S') for ts in timestamps]
                time_objects.sort()
                
                active_duration = (time_objects[-1] - time_objects[0]).total_seconds() / 60
                active_duration = max(active_duration, 1.0)
                total_duration += active_duration
                
            except Exception:
                total_duration += 1.0
        
        print(f"[SERVICE] real_total_session_duration: {total_duration:.2f} minutos")
        return round(total_duration, 2)
        
    except Exception as e:
        print(f"[SERVICE] Erro ao calcular tempo total real: {e}")
        return 0.0

def calculate_attendance_ratio(traces, lecture_id):
    """
    Calcula a % do tempo que os alunos ficaram vs duração total da aula
    """
    try:
        # Tempo real médio que alunos ficaram
        avg_real_session = calculate_real_avg_session_per_student(traces)
        
        # Duração oficial da aula
        lecture_duration = calculateTotalTimeWatched(lecture_id)
        
        if lecture_duration <= 0:
            return 0.0
        
        attendance_ratio = avg_real_session / lecture_duration
        
        # Limita entre 0 e 1 (100%)
        attendance_ratio = max(0.0, min(attendance_ratio, 1.0))
        
        print(f"[SERVICE] attendance_ratio: {attendance_ratio:.1%} ({avg_real_session:.1f}min / {lecture_duration:.1f}min)")
        
        return round(attendance_ratio, 3)
        
    except Exception as e:
        print(f"[SERVICE] Erro ao calcular attendance_ratio: {e}")
        return 0.0    