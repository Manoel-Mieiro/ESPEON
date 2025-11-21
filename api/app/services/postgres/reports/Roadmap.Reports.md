1. ENGAGEMENT BÁSICO
metrics['total_students'] = len(unique_students)
metrics['total_session_duration'] = total_time  # tempo total de sessão
metrics['avg_session_per_student'] = avg_session_time

2. FOCO NA AULA (Core)
metrics['lecture_focus_ratio'] = 0.65  # 65% do tempo na aba da aula
metrics['avg_focus_duration'] = 12.5   # em minutos - tempo médio contínuo focado
metrics['max_focus_duration'] = 25.3   # maior período de foco ininterrupto

3. DISTRAÇÕES
metrics['distraction_ratio'] = 0.35    # 35% do tempo em distrações
metrics['distraction_frequency'] = 8.2 # trocas para distração por hora
metrics['main_distractions'] = {       # ranking de distrações
    'chatgpt': 0.15,
    'github': 0.10, 
    'extensions': 0.08,
    'other': 0.02
}

4. COMPORTAMENTO DE MULTITASKING
metrics['tab_switch_frequency'] = 15.3  # trocas de aba por hora
metrics['multitasking_intensity'] = 0.42 # escala 0-1 de multitasking
metrics['focus_fragmentation'] = 6.8    # segmentos de foco por hora

5. PARTICIPAÇÃO ATIVA
metrics['camera_engagement'] = 0.25     # % tempo com câmera ativa
metrics['mic_engagement'] = 0.18        # % tempo com microfone ativo  
metrics['voluntary_participation'] = 0.32 # % sessão com participação ativa

6. PADRÕES TEMPORAIS
metrics['engagement_trend'] = {         # engajamento por quartis da aula
    'q1': 0.72,    # primeiro quarto
    'q2': 0.65, 
    'q3': 0.58,
    'q4': 0.48     # último quarto
}
metrics['peak_engagement_time'] = "14:15" # horário de pico de foco
metrics['dropoff_point'] = "00:42:15"     # quando engajamento cai 50%

7. SCORES COMPOSTOS
metrics['engagement_score'] = 0.68      # score geral 0-1
metrics['attention_health'] = 0.72      # saúde do padrão de atenção
metrics['distraction_risk'] = 0.45      # risco de distração (0-1)


📈 VISUALIZAÇÃO SUGERIDA
ENGAGEMENT OVERVIEW:
═══════════════════════════════════════
🎯 Focus Ratio:    ██████████ 65%
📱 Distractions:   █████ 35% 
🔄 Tab Switching:  15.3/hr
🎥 Participation:  25%

ATTENTION PATTERN:
[███████▒▒▒▒] Q1 - 72% focus
[██████▒▒▒▒▒] Q2 - 65% focus  
[█████▒▒▒▒▒▒] Q3 - 58% focus
[████▒▒▒▒▒▒▒] Q4 - 48% focus

TOP DISTRACTIONS:
ChatGPT    █████████████ 45%
GitHub     █████████ 30%
Extensions █████ 15%
Other      ██ 10%


🔍 ANÁLISES DERIVADAS
# Insights automáticos
metrics['insights'] = [
    "High engagement in first 30 minutes",
    "ChatGPT is main distraction source", 
    "Attention drops significantly after 40min",
    "Camera usage below class average"
]

# Recomendações
metrics['recommendations'] = [
    "Consider breaks at 40min mark",
    "Encourage camera usage in Q2",
    "Monitor ChatGPT usage patterns"
]