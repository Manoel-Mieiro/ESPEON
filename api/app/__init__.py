from flask import Flask
from app.routes.traces import traces_bp
from app.routes.users import users_bp
from app.routes.login import login_bp
from app.routes.lectures import lectures_bp
from app.routes.subject import subjects_bp
from app.routes.reports import report_bp
from app.routes.reportsStudent import report_student_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(traces_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(lectures_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(report_student_bp)
    return app
