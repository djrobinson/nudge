# services/web/server/__init__.py

from dotenv import load_dotenv
load_dotenv()

import os

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

from server.api import views


def create_app():
    app_settings = os.getenv(
        'APP_SETTINGS',
        'project.server.config.DevelopmentConfig'
    )
    app = Flask(
        __name__,
        template_folder='../client/templates',
        static_folder='../client/static'
    )
    app.config.from_object(app_settings)

    socketio.init_app(app, async_mode='eventlet')

    # Register web application routes
    from server.api.views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
