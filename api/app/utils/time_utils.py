import os
from datetime import datetime, time, date, timezone, timedelta

def get_current_datetime():
    """
    Retorna o datetime atual baseado na configuração de HOSTING
    Se HOSTING = 'render', retorna UTC-3, caso contrário retorna UTC
    """
    hosting = os.getenv('HOSTING', '').lower()
    
    if hosting == 'render':
        tz = timezone(timedelta(hours=-3))
        return datetime.now(tz)
    else:
        return datetime.now(timezone.utc)

def get_current_utc():
    """Sempre retorna UTC (para casos onde você precisa de UTC independente do HOSTING)"""
    return datetime.now(timezone.utc)

def convert_time_objects_to_string(data: dict) -> dict:
    """
    Converte objetos time, datetime, date e Decimal para string no formato ISO.
    """
    def convert_value(value):
        if value is None:
            return None
        elif hasattr(value, 'isoformat') and callable(value.isoformat):
            try:
                return value.isoformat()
            except:
                return str(value)
        # Handle Decimal objects from PostgreSQL
        elif hasattr(value, 'as_integer_ratio'):  # Decimal and float
            return float(value)
        elif isinstance(value, dict):
            return convert_time_objects_to_string(value)
        elif isinstance(value, list):
            return [convert_value(item) for item in value]
        elif isinstance(value, tuple):
            return [convert_value(item) for item in value]
        else:
            return value
    
    if not isinstance(data, dict):
        return data
        
    result = {}
    for key, value in data.items():
        result[key] = convert_value(value)
    return result

