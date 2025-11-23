def calculate_engagement_score(metrics_dict):
    """
    Calcula um score geral de engajamento (0-1) baseado em múltiplas métricas
    """
    try:
        # Fatores que contribuem para o engajamento
        factors = {
            # Peso alto
            'focus_ratio': metrics_dict.get('lecture_focus_ratio', 0.0),
            # Peso alto
            'attendance_ratio': metrics_dict.get('attendance_ratio', 0.0),
            # Peso médio
            'participation': metrics_dict.get('voluntary_participation', 0.0),
            # Peso baixo
            'camera_engagement': metrics_dict.get('camera_engagement', 0.0),
            # Peso baixo
            'mic_engagement': metrics_dict.get('mic_engagement', 0.0),
        }

        # Pesos para cada fator
        weights = {
            'focus_ratio': 0.35,      # 35% - Foco é o mais importante
            'attendance_ratio': 0.30,  # 30% - Presença é fundamental
            'participation': 0.20,     # 20% - Participação ativa
            'camera_engagement': 0.10,  # 10% - Engajamento visual
            'mic_engagement': 0.05,    # 5%  - Participação vocal
        }

        # Calcula score ponderado
        engagement_score = 0.0
        for factor, value in factors.items():
            engagement_score += value * weights[factor]

        # Ajusta para garantir que está entre 0 e 1
        engagement_score = max(0.0, min(engagement_score, 1.0))

        print(f"[SCORE] engagement_score: {engagement_score:.3f}")
        print(f"[SCORE] Fatores: foco={factors['focus_ratio']:.1%}, "
              f"presença={factors['attendance_ratio']:.1%}, "
              f"participação={factors['participation']:.1%}")

        return round(engagement_score, 3)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular engagement_score: {e}")
        return 0.0


def calculate_attention_health(metrics_dict):
    """
    Calcula a saúde do padrão de atenção (0-1)
    Considera sustentação do foco e baixa fragmentação
    """
    try:
        # Fatores que indicam saúde da atenção
        factors = {
            'focus_duration_health': calculate_focus_duration_health(
                metrics_dict.get('avg_focus_duration', 0.0)
            ),
            'fragmentation_health': calculate_fragmentation_health(
                metrics_dict.get('focus_fragmentation', 0.0)
            ),
            'multitasking_health': calculate_multitasking_health(
                metrics_dict.get('multitasking_intensity', 0.0)
            ),
            'consistency_health': calculate_consistency_health(
                metrics_dict.get('engagement_trend', {})
            )
        }

        # Pesos para saúde da atenção
        weights = {
            'focus_duration_health': 0.30,    # 30% - Duração do foco
            'fragmentation_health': 0.25,     # 25% - Baixa fragmentação
            'multitasking_health': 0.25,      # 25% - Baixo multitasking
            'consistency_health': 0.20,       # 20% - Consistência temporal
        }

        # Calcula score ponderado
        attention_health = 0.0
        for factor, value in factors.items():
            attention_health += value * weights[factor]

        attention_health = max(0.0, min(attention_health, 1.0))

        print(f"[SCORE] attention_health: {attention_health:.3f}")
        print(f"[SCORE] Saúde: foco={factors['focus_duration_health']:.1%}, "
              f"fragmentação={factors['fragmentation_health']:.1%}, "
              f"multitasking={factors['multitasking_health']:.1%}")

        return round(attention_health, 3)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular attention_health: {e}")
        return 0.0


def calculate_focus_duration_health(avg_focus_duration):
    """
    Avalia saúde baseada na duração média do foco
    """
    # Foco ideal: 15-20 minutos (baseado em ciclos de atenção)
    if avg_focus_duration >= 15.0:
        return 1.0  # Excelente
    elif avg_focus_duration >= 10.0:
        return 0.7  # Bom
    elif avg_focus_duration >= 5.0:
        return 0.4  # Regular
    else:
        return 0.1  # Ruim


def calculate_fragmentation_health(focus_fragmentation):
    """
    Avalia saúde baseada na fragmentação do foco
    """
    # Fragmentação ideal: < 5 segmentos/hora
    if focus_fragmentation <= 5.0:
        return 1.0  # Excelente
    elif focus_fragmentation <= 8.0:
        return 0.7  # Bom
    elif focus_fragmentation <= 12.0:
        return 0.4  # Regular
    else:
        return 0.1  # Ruim


def calculate_multitasking_health(multitasking_intensity):
    """
    Avalia saúde baseada na intensidade de multitasking
    """
    # Multitasking ideal: < 0.3
    if multitasking_intensity <= 0.3:
        return 1.0  # Excelente
    elif multitasking_intensity <= 0.5:
        return 0.7  # Bom
    elif multitasking_intensity <= 0.7:
        return 0.4  # Regular
    else:
        return 0.1  # Ruim


def calculate_consistency_health(engagement_trend):
    """
    Avalia saúde baseada na consistência do engajamento
    """
    try:
        if not engagement_trend:
            return 0.5  # Neutro se não há dados

        q1 = engagement_trend.get('q1', 0.0)
        q4 = engagement_trend.get('q4', 0.0)

        # Quanto menor a queda, melhor a consistência
        engagement_drop = q1 - q4

        if engagement_drop <= 0.1:    # Queda <= 10%
            return 1.0
        elif engagement_drop <= 0.2:  # Queda <= 20%
            return 0.7
        elif engagement_drop <= 0.3:  # Queda <= 30%
            return 0.4
        else:                         # Queda > 30%
            return 0.1

    except Exception:
        return 0.5


def calculate_distraction_risk(metrics_dict):
    """
    Calcula o risco de distração (0-1) - quanto maior, mais distraído
    """
    try:
        # Fatores que contribuem para o risco de distração
        risk_factors = {
            'distraction_ratio': metrics_dict.get('distraction_ratio', 0.0),
            'distraction_frequency': metrics_dict.get('distraction_frequency', 0.0),
            'main_distraction_strength': calculate_main_distraction_strength(
                metrics_dict.get('main_distractions', {})
            ),
            'tab_switch_intensity': calculate_tab_switch_intensity(
                metrics_dict.get('tab_switch_frequency', 0.0)
            )
        }

        # Pesos para risco de distração
        weights = {
            'distraction_ratio': 0.40,           # 40% - Tempo em distrações
            'distraction_frequency': 0.25,       # 25% - Frequência de distrações
            'main_distraction_strength': 0.20,   # 20% - Força das distrações principais
            'tab_switch_intensity': 0.15,        # 15% - Intensidade de trocas
        }

        # Calcula risco ponderado
        distraction_risk = 0.0
        for factor, value in risk_factors.items():
            distraction_risk += value * weights[factor]

        distraction_risk = max(0.0, min(distraction_risk, 1.0))

        print(f"[SCORE] distraction_risk: {distraction_risk:.3f}")
        print(f"[SCORE] Riscos: ratio={risk_factors['distraction_ratio']:.1%}, "
              f"frequência={risk_factors['distraction_frequency']:.1%}")

        return round(distraction_risk, 3)

    except Exception as e:
        print(f"[SERVICE] Erro ao calcular distraction_risk: {e}")
        return 0.0


def calculate_main_distraction_strength(main_distractions):
    """
    Calcula a força das distrações principais
    """
    try:
        if not main_distractions:
            return 0.0

        # Soma as porcentagens das distrações principais (excluindo 'other')
        total_strength = 0.0
        for distraction, percentage in main_distractions.items():
            if distraction != 'other':
                total_strength += percentage

        return min(total_strength, 1.0)  # Limita a 1.0

    except Exception:
        return 0.0


def calculate_tab_switch_intensity(tab_switch_frequency):
    """
    Converte frequência de trocas em intensidade (0-1)
    """
    # Normaliza baseado em frequência máxima esperada (30/hora)
    return min(tab_switch_frequency / 30.0, 1.0)
