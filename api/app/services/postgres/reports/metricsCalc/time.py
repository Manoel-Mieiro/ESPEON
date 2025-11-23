from app.services.postgres.lectures import findOneLecture
from datetime import datetime

from app.services.postgres.reports.metricsCalc.utils import (
    is_lecture_tab,
    get_time_diff_minutes,
    get_lecture_periods,
)


def calculate_engagement_trend(traces, lecture_id):
    """
    Calcula o engajamento por quartis usando datetime.datetime
    """
    try:
        print(f"[DEBUG] Iniciando cálculo de engagement trend para lecture_id: {lecture_id}")
        print(f"[DEBUG] Número de traces recebidos: {len(traces)}")
        
        # Obtém os períodos E A DATA REAL da aula
        lecture_data = findOneLecture(lecture_id)
        if not lecture_data:
            print("[DEBUG] Aula não encontrada, retornando zeros")
            return {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
        
        date_lecture = lecture_data.get("date_lecture")
        period_start = lecture_data.get("period_start")
        period_end = lecture_data.get("period_end")
        
        print(f"[DEBUG] Data da aula: {date_lecture}, Horário: {period_start} às {period_end}")
        
        if not date_lecture or not period_start or not period_end:
            print("[DEBUG] Dados da aula incompletos, retornando zeros")
            return {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
        
        # Cria datetime REAL para início e fim da aula
        start_dt = datetime.strptime(f"{date_lecture} {period_start}", "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(f"{date_lecture} {period_end}", "%Y-%m-%d %H:%M:%S")
        
        # Ajuste se a aula terminar depois da meia-noite
        if end_dt < start_dt:
            end_dt = end_dt.replace(day=end_dt.day + 1)
        
        print(f"[TEMPO] Aula REAL: \n INICIO:{start_dt}\n FIM:{end_dt}")
        
        # Calcula duração total em minutos
        lecture_duration = (end_dt - start_dt).total_seconds() / 60
        print(f"[TEMPO] lecture_duration: {lecture_duration}")

        if lecture_duration <= 0:
            print(f"[DEBUG] Duração da aula <= 0: {lecture_duration}, retornando zeros")
            return {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
        
        # Define quartis
        quartile_duration = lecture_duration / 4
        print(f"[TEMPO] quartile_duration: {quartile_duration}")
        quartiles = {
            'q1': (0, quartile_duration),
            'q2': (quartile_duration, quartile_duration * 2),
            'q3': (quartile_duration * 2, quartile_duration * 3),
            'q4': (quartile_duration * 3, lecture_duration)
        }
        
        print(f"[DEBUG] Quartis definidos: {quartiles}")
        
        # Contadores
        quartile_data = {q: {'focus': 0.0, 'total': 0.0} for q in quartiles}
        
        # Processa traces - ordena por timestamp
        sorted_traces = sorted(traces, key=lambda x: x.get('timestamp', ''))
        print(f"[DEBUG] Número de traces após ordenação: {len(sorted_traces)}")
        
        # Mostra alguns traces para debug
        print(f"[DEBUG] Primeiros 5 traces:")
        for i, trace in enumerate(sorted_traces[:5]):
            print(f"  Trace {i}: timestamp={trace.get('timestamp')}")
        
        if len(sorted_traces) <= 1:
            print("[DEBUG] Poucos traces para processar (<= 1), retornando zeros")
            return {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
        
        traces_processados = 0
        traces_fora_do_horario = 0
        time_diff_zero_ou_negativo = 0
        erro_conversao_timestamp = 0
        
        for i in range(1, len(sorted_traces)):
            prev_trace = sorted_traces[i-1]
            curr_trace = sorted_traces[i]
            
            prev_timestamp = prev_trace.get('timestamp')
            curr_timestamp = curr_trace.get('timestamp')
            
            # PULA traces sem timestamp
            if not prev_timestamp or not curr_timestamp:
                continue
            
            time_diff = get_time_diff_minutes(prev_timestamp, curr_timestamp)
            
            if time_diff <= 0:
                time_diff_zero_ou_negativo += 1
                continue
            
            # CONVERTE timestamp do trace usando a DATA REAL da aula
            try:
                # Combina a data da aula com a hora do trace
                trace_dt = datetime.strptime(f"{date_lecture} {prev_timestamp}", "%Y-%m-%d %H:%M:%S")
                print(f"[DEBUG] Trace {i-1}: {trace_dt}")
                
            except Exception as e:
                erro_conversao_timestamp += 1
                print(f"[DEBUG] Erro ao converter timestamp '{prev_timestamp}': {e}")
                continue
            
            # Calcula minutos desde o início da aula
            minutes_from_start = (trace_dt - start_dt).total_seconds() / 60
            print(f"[DEBUG] Minutes from start: {minutes_from_start}")
            
            # Se fora do horário da aula, ignora
            if minutes_from_start < 0:
                traces_fora_do_horario += 1
                print(f"[DEBUG] Trace ANTES do início da aula: {minutes_from_start} min")
                continue
                
            if minutes_from_start > lecture_duration:
                traces_fora_do_horario += 1
                print(f"[DEBUG] Trace DEPOIS do fim da aula: {minutes_from_start} min (duraçao: {lecture_duration} min)")
                continue
            
            # Determina quartil
            quartil_encontrado = False
            for quartile, (q_start, q_end) in quartiles.items():
                if q_start <= minutes_from_start < q_end:
                    quartile_data[quartile]['total'] += time_diff
                    is_focus = is_lecture_tab(prev_trace)
                    if is_focus:
                        quartile_data[quartile]['focus'] += time_diff
                    traces_processados += 1
                    quartil_encontrado = True
                    print(f"[DEBUG] → Quartil {quartile}: focus={is_focus}, time_diff={time_diff}")
                    break
            
            if not quartil_encontrado:
                print(f"[DEBUG] Trace não atribuído a nenhum quartil: minutes_from_start={minutes_from_start}")
        
        print(f"[DEBUG] Estatísticas finais do processamento:")
        print(f"[DEBUG] - Traces processados com sucesso: {traces_processados}")
        print(f"[DEBUG] - Traces fora do horário: {traces_fora_do_horario}")
        print(f"[DEBUG] - Time diffs zero/negativos: {time_diff_zero_ou_negativo}")
        print(f"[DEBUG] - Erros de conversão de timestamp: {erro_conversao_timestamp}")
        print(f"[DEBUG] - Dados por quartil antes do cálculo: {quartile_data}")
        
        # Calcula ratios
        engagement_trend = {}
        for quartile, data in quartile_data.items():
            if data['total'] > 0:
                engagement_trend[quartile] = round(data['focus'] / data['total'], 3)
                print(f"[DEBUG] Quartil {quartile}: focus={data['focus']}, total={data['total']}, ratio={engagement_trend[quartile]}")
            else:
                engagement_trend[quartile] = 0.0
                print(f"[DEBUG] Quartil {quartile}: total=0, ratio=0.0")
        
        print(f"[SERVICE] engagement_trend final: {engagement_trend}")
        return engagement_trend
        
    except Exception as e:
        print(f"[SERVICE] Erro ao calcular engagement_trend: {e}")
        import traceback
        print(f"[SERVICE] Traceback: {traceback.format_exc()}")
        return {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}

def get_lecture_start_time(lecture_id):
    """
    Obtém o horário de início da aula a partir dos dados da lecture
    """
    try:
        lecture = findOneLecture(lecture_id)
        
        if not lecture:
            print(f"[SERVICE] Aula {lecture_id} não encontrada")
            return None
        
        period_start = lecture.get("period_start")
        
        if not period_start:
            print(f"[SERVICE] period_start não encontrado para aula {lecture_id}")
            return None
        
        # Converte para datetime.time se for string
        if isinstance(period_start, str):
            return datetime.strptime(period_start, "%H:%M:%S").time()
        elif isinstance(period_start, datetime):
            return period_start.time()
        else:
            print(f"[SERVICE] Formato inválido para period_start: {type(period_start)}")
            return None
            
    except Exception as e:
        print(f"[SERVICE] Erro ao obter horário de início da aula {lecture_id}: {e}")
        return None

def calculate_peak_engagement_time(traces, lecture_id):
    """
    Identifica o horário com maior concentração de foco na aula
    """
    try:
        # Obtém os períodos como datetime.datetime
        start_dt, end_dt = get_lecture_periods(lecture_id)
        if not start_dt or not end_dt:
            return "N/A"
        
        # Agrupa foco por intervalos de 5 minutos
        focus_by_interval = {}
        
        sorted_traces = sorted(traces, key=lambda x: x.get('timestamp', ''))
        
        for i in range(1, len(sorted_traces)):
            prev_trace = sorted_traces[i-1]
            curr_trace = sorted_traces[i]
            
            time_diff = get_time_diff_minutes(
                prev_trace.get('timestamp'), 
                curr_trace.get('timestamp')
            )
            
            if time_diff <= 0:
                continue
            
            # Converte timestamp do trace
            trace_time_str = prev_trace.get('timestamp')
            trace_time = datetime.combine(
                start_dt.date(),
                datetime.strptime(trace_time_str, '%H:%M:%S').time()
            )
            
            # Horário real (sem considerar início da aula)
            interval_key = trace_time.strftime('%H:%M')
            
            if interval_key not in focus_by_interval:
                focus_by_interval[interval_key] = 0.0
            
            # Adiciona tempo focado neste intervalo
            if is_lecture_tab(prev_trace):
                focus_by_interval[interval_key] += time_diff
        
        # Encontra o intervalo com maior foco
        if focus_by_interval:
            peak_time = max(focus_by_interval.items(), key=lambda x: x[1])[0]
            print(f"[SERVICE] peak_engagement_time: {peak_time}")
            return peak_time
        else:
            return "N/A"
            
    except Exception as e:
        print(f"[SERVICE] Erro ao calcular peak_engagement_time: {e}")
        return "N/A"
    
def calculate_dropoff_point(traces, lecture_id):
    """
    Identifica quando o engajamento cai para metade do pico
    """
    try:
        print(f"[DEBUG] Iniciando cálculo de dropoff_point para lecture_id: {lecture_id}")
        
        # Obtém os períodos E A DATA REAL da aula
        lecture_data = findOneLecture(lecture_id)
        if not lecture_data:
            print("[DEBUG] Aula não encontrada, retornando N/A")
            return "N/A"
        
        date_lecture = lecture_data.get("date_lecture")
        period_start = lecture_data.get("period_start")
        period_end = lecture_data.get("period_end")
        
        print(f"[DEBUG] Data da aula: {date_lecture}, Horário: {period_start} às {period_end}")
        
        if not date_lecture or not period_start or not period_end:
            print("[DEBUG] Dados da aula incompletos, retornando N/A")
            return "N/A"
        
        # Cria datetime REAL para início e fim da aula
        start_dt = datetime.strptime(f"{date_lecture} {period_start}", "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(f"{date_lecture} {period_end}", "%Y-%m-%d %H:%M:%S")
        
        # Ajuste se a aula terminar depois da meia-noite
        if end_dt < start_dt:
            end_dt = end_dt.replace(day=end_dt.day + 1)
        
        print(f"[TEMPO] Aula REAL: \n INICIO:{start_dt}\n FIM:{end_dt}")
        
        # Calcula duração total
        lecture_duration = (end_dt - start_dt).total_seconds() / 60
        
        if lecture_duration <= 0:
            print(f"[DEBUG] Duração da aula <= 0: {lecture_duration}, retornando N/A")
            return "N/A"
        
        print(f"[DEBUG] Duração da aula: {lecture_duration} minutos")
        
        # Calcula engajamento por intervalos de 5 minutos
        engagement_by_time = {}
        
        sorted_traces = sorted(traces, key=lambda x: x.get('timestamp', ''))
        print(f"[DEBUG] Número de traces para processar: {len(sorted_traces)}")
        
        traces_processados = 0
        traces_fora_do_horario = 0
        
        for i in range(1, len(sorted_traces)):
            prev_trace = sorted_traces[i-1]
            curr_trace = sorted_traces[i]
            
            time_diff = get_time_diff_minutes(
                prev_trace.get('timestamp'), 
                curr_trace.get('timestamp')
            )
            
            if time_diff <= 0:
                continue
            
            # CORREÇÃO: Usa a data real da aula para converter o timestamp do trace
            trace_time_str = prev_trace.get('timestamp')
            try:
                trace_dt = datetime.strptime(f"{date_lecture} {trace_time_str}", "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"[DEBUG] Erro ao converter timestamp {trace_time_str}: {e}")
                continue
            
            # Tempo desde o início da aula
            minutes_from_start = (trace_dt - start_dt).total_seconds() / 60
            
            if minutes_from_start < 0 or minutes_from_start > lecture_duration:
                traces_fora_do_horario += 1
                continue
            
            interval_key = int(minutes_from_start // 5) * 5  # Intervalos de 5 minutos
            
            if interval_key not in engagement_by_time:
                engagement_by_time[interval_key] = {'focus': 0.0, 'total': 0.0}
            
            engagement_by_time[interval_key]['total'] += time_diff
            if is_lecture_tab(prev_trace):
                engagement_by_time[interval_key]['focus'] += time_diff
            
            traces_processados += 1
        
        print(f"[DEBUG] Estatísticas do processamento:")
        print(f"[DEBUG] - Traces processados: {traces_processados}")
        print(f"[DEBUG] - Traces fora do horário: {traces_fora_do_horario}")
        print(f"[DEBUG] - Intervalos com dados: {len(engagement_by_time)}")
        
        # Calcula ratio de engajamento por intervalo
        engagement_ratios = {}
        for interval, data in engagement_by_time.items():
            if data['total'] > 0:
                engagement_ratios[interval] = data['focus'] / data['total']
                print(f"[DEBUG] Intervalo {interval}min: focus={data['focus']:.2f}, total={data['total']:.2f}, ratio={engagement_ratios[interval]:.3f}")
        
        if not engagement_ratios:
            print("[DEBUG] Nenhum intervalo com dados, retornando N/A")
            return "N/A"
        
        # Encontra o pico de engajamento
        peak_engagement = max(engagement_ratios.values())
        peak_threshold = peak_engagement * 0.5  # 50% do pico
        
        print(f"[DEBUG] Pico de engajamento: {peak_engagement:.3f}")
        print(f"[DEBUG] Threshold (50% do pico): {peak_threshold:.3f}")
        
        # Encontra o primeiro ponto onde o engajamento cai abaixo do threshold
        sorted_intervals = sorted(engagement_ratios.keys())
        dropoff_minute = None
        
        print(f"[DEBUG] Intervalos ordenados: {sorted_intervals}")
        
        for interval in sorted_intervals:
            ratio = engagement_ratios[interval]
            print(f"[DEBUG] Verificando intervalo {interval}min: ratio={ratio:.3f}, threshold={peak_threshold:.3f}")
            
            if ratio < peak_threshold:
                # Verifica se é uma queda sustentada (próximos 2 intervalos também abaixo)
                sustained_drop = True
                check_intervals = 0
                
                for next_interval in range(interval + 5, min(interval + 20, max(sorted_intervals) + 1), 5):
                    if next_interval in engagement_ratios:
                        check_intervals += 1
                        if engagement_ratios[next_interval] >= peak_threshold:
                            sustained_drop = False
                            print(f"[DEBUG] Queda não sustentada: intervalo {next_interval}min tem ratio {engagement_ratios[next_interval]:.3f}")
                            break
                
                # Se não encontrou intervalos suficientes para verificar, considera sustentada
                if check_intervals < 2:
                    sustained_drop = True
                
                if sustained_drop:
                    dropoff_minute = interval
                    print(f"[DEBUG] Dropoff encontrado no intervalo {interval}min (ratio={ratio:.3f})")
                    break
        
        if dropoff_minute is not None:
            # Converte para formato HH:MM:SS
            total_minutes = int(dropoff_minute)
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            dropoff_time = f"{hours:02d}:{minutes:02d}:00"
            print(f"[SERVICE] dropoff_point: {dropoff_time} (aos {dropoff_minute:.0f} minutos)")
            return dropoff_time
        else:
            print("[DEBUG] Nenhum dropoff point encontrado")
            return "N/A"
            
    except Exception as e:
        print(f"[SERVICE] Erro ao calcular dropoff_point: {e}")
        import traceback
        print(f"[SERVICE] Traceback: {traceback.format_exc()}")
        return "N/A"