import os
import datetime

def get_current_datetime():
    """
    Retorna o datetime atual baseado na configuração de HOSTING
    Se HOSTING = 'render', retorna UTC-3, caso contrário retorna UTC
    """
    hosting = os.getenv('HOSTING', '').lower()
    
    if hosting == 'render':
        tz = datetime.timezone(datetime.timedelta(hours=-3))
        return datetime.datetime.now(tz)
    else:
        return datetime.datetime.now(datetime.timezone.utc)

def get_current_utc():
    """Sempre retorna UTC (para casos onde você precisa de UTC independente do HOSTING)"""
    return datetime.datetime.now(datetime.timezone.utc)