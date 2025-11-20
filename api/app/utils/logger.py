import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import json

class FlaskLogger:
    def __init__(self, name='FlaskApp'):
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_logger(self):
        # Remove handlers existentes para evitar duplicação
        if self.logger.handlers:
            self.logger.handlers.clear()

        env = os.getenv('APP_ENV', 'DSV')
        log_level = logging.DEBUG if env == 'DSV' else logging.INFO
        
        self.logger.setLevel(log_level)

        # Formato do log
        formatter = logging.Formatter(
            f'[%(asctime)s] 🔵 {os.getenv("APP_ENV", "DSV")} - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Handler para arquivo (apenas em PRD no Render)
        if env == 'PRD' and os.getenv('HOSTING') == 'render':
            os.makedirs('logs', exist_ok=True)
            file_handler = RotatingFileHandler(
                'logs/app.log',
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message, extra_data=None):
        self._log('DEBUG', message, extra_data)

    def info(self, message, extra_data=None):
        self._log('INFO', message, extra_data)

    def warn(self, message, extra_data=None):
        self._log('WARNING', message, extra_data)

    def error(self, message, extra_data=None):
        self._log('ERROR', message, extra_data)

    def api_request(self, method, endpoint, status_code, response_time=None, user_id=None, client_ip=None):
        extra_data = {
            'method': method,
            'endpoint': endpoint,
            'status_code': status_code,
            'response_time': response_time,
            'user_id': user_id,
            'client_ip': client_ip,
            'type': 'api_request'
        }
        level = 'INFO' if status_code < 400 else 'WARNING'
        self._log(level, f'API {method} {endpoint} - {status_code}', extra_data)

    def db_operation(self, operation, table, duration=None, rows_affected=None, db_type=None):
        extra_data = {
            'operation': operation,
            'table': table,
            'duration': duration,
            'rows_affected': rows_affected,
            'db_type': db_type or 'postgres',
            'type': 'db_operation'
        }
        self._log('DEBUG', f'DB {operation} on {table}', extra_data)

    def trace_event(self, event_type, student_email, lecture_id, details=None):
        extra_data = {
            'event_type': event_type,
            'student_email': student_email,
            'lecture_id': lecture_id,
            'details': details,
            'type': 'trace_event'
        }
        self._log('INFO', f'TRACE: {event_type} - {student_email}', extra_data)

    def mongo_operation(self, operation, collection, duration=None, documents_affected=None):
        extra_data = {
            'operation': operation,
            'collection': collection,
            'duration': duration,
            'documents_affected': documents_affected,
            'db_type': 'mongodb',
            'type': 'db_operation'
        }
        self._log('DEBUG', f'MONGO {operation} on {collection}', extra_data)

    def startup(self, message, config=None):
        extra_data = {
            'port': os.getenv('FLASK_RUN_PORT'),
            'app_env': os.getenv('APP_ENV'),
            'hosting': os.getenv('HOSTING'),
            'database': 'postgres' if os.getenv('DATABASE_URL') else 'mongodb',
            'type': 'startup',
            'config': config
        }
        self._log('INFO', message, extra_data)

    def _log(self, level, message, extra_data=None):
        log_message = message
        if extra_data:
            log_message += f" | {json.dumps(extra_data, default=str)}"
        
        if level == 'DEBUG':
            self.logger.debug(log_message)
        elif level == 'INFO':
            self.logger.info(log_message)
        elif level == 'WARNING':
            self.logger.warning(log_message)
        elif level == 'ERROR':
            self.logger.error(log_message)

app_logger = FlaskLogger('FlaskApp')
api_logger = FlaskLogger('API')
db_logger = FlaskLogger('Database')
trace_logger = FlaskLogger('Traces')
auth_logger = FlaskLogger('Auth')
mongo_logger = FlaskLogger('MongoDB')