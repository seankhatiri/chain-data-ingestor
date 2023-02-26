import os
from importlib import import_module
from threading import Timer
from time import sleep

from flask import Flask, request, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from logic.controller.construct_graph_controler import ConstructGraphControler
from logic.controller.search_controler import SearchControler
from configuration.configs import Configs

template_dir = os.path.abspath('templates')

db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app_):
    db.init_app(app_)
    login_manager.init_app(app_)


def configure_database(app_):
    @app_.before_first_request
    def initialize_database():
        db.create_all()

    @app_.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def register_blueprints(app_):
    for module_name in ('base', 'dashboard'):
        module = import_module('flask_app.{}.routes'.format(module_name))
        app_.register_blueprint(module.blueprint)


def create_app(config):
    _app = Flask(__name__, static_folder='base/static')
    _app.config.from_object(config)
    register_extensions(_app)
    register_blueprints(_app)
    configure_database(_app)
    controller = ConstructGraphControler()
    if Configs.mode == 'stage':
        pass
    elif Configs.mode == 'test':
        pass
    else:
        pass

    return _app
