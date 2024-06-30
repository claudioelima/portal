from flask import Flask
from app.routes.routes import routes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    app.register_blueprint(routes)
    return app
