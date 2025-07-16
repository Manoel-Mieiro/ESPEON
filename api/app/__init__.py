from flask import Flask
from app.routes.traces import traces_bp
from app.routes.users import users_bp
from app.routes.login import login_bp
from app.routes.lectures import lectures_bp
from app.routes.lectures2 import lectures2_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(traces_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(lectures_bp)
    app.register_blueprint(lectures2_bp)
    return app
