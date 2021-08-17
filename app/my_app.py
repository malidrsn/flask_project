from flask import Flask
from .views import home


def create_app():
    app = Flask(__name__, template_folder="templates")

    app.register_blueprint(home.bp)

    return app
