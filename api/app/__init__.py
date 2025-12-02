from flask import Flask, request, g
from flask_restx import Api
import time
import os
from app.utils.logger import app_logger, api_logger
from app.routes.traces import traces_bp, traces_ns
from app.routes.users import users_bp, users_ns
from app.routes.login import login_bp, login_ns
from app.routes.lectures import lectures_bp, lectures_ns
from app.routes.subject import subjects_bp, subjects_ns
from app.routes.reports import report_bp, report_ns
from app.routes.reportsStudent import report_student_bp

def create_app():
    app = Flask(__name__)
    
    # Configurar Swagger API
    api = Api(
        app,
        version='1.0',
        title='ESPEON API',
        description='API para análise de atenção e engajamento em aulas online',
        doc='/docs/',  
        prefix='/api/v1',
        contact='Manoel Mieiro',
        contact_email='17733635730@cefet-rj.br'
    )
    
    
    
    api.add_namespace(report_ns, path='/reports')   
    api.add_namespace(login_ns, path='/auth') 
    api.add_namespace(subjects_ns, path='/subjects') 
    api.add_namespace(traces_ns, path='/traces') 
    api.add_namespace(lectures_ns, path='/lectures') 
    api.add_namespace(users_ns, path='/users') 
    
    app_logger.startup("Inicializando aplicação Flask", {
        'port': os.getenv('FLASK_RUN_PORT'),
        'environment': os.getenv('APP_ENV'),
        'hosting': os.getenv('HOSTING'),
        'database_url_configured': bool(os.getenv('DATABASE_URL')),
        'mongo_configured': bool(os.getenv('MONGO_URI')),
        'blueprints_count': 7,
        'swagger_enabled': True,
        'swagger_url': '/docs/'
    })
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
        if os.getenv('APP_ENV') == 'DSV':  
            api_logger.debug(f"Incoming request: {request.method} {request.path}", {
                'client_ip': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            })

    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            response_time = round((time.time() - g.start_time) * 1000, 2)  # ms
            
            api_logger.api_request(
                method=request.method,
                endpoint=request.path,
                status_code=response.status_code,
                response_time=response_time,
                user_id=getattr(g, 'user_id', None),
                client_ip=request.remote_addr
            )
        
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        app_logger.error(f"Unhandled exception: {str(e)}", {
            'exception_type': type(e).__name__,
            'path': request.path,
            'method': request.method,
            'client_ip': request.remote_addr
        })
        return {"error": "Internal server error"}, 500

    app.register_blueprint(traces_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(lectures_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(report_student_bp)
    
    app_logger.startup("Flask application initialized successfully", {
        'registered_blueprints': [
            'traces_bp',
            'users_bp', 
            'login_bp',
            'lectures_bp',
            'subjects_bp',
            'report_bp',
            'report_student_bp'
        ],
        'swagger_namespaces': [
            'report_ns'
        ]
    })
    
    return app