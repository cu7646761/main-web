from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from elasticsearch import Elasticsearch
from config import config
# from app.cache import cache
from flask_bcrypt import Bcrypt

db = MongoEngine()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    bcrypt.init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    # cache.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.main.auth.views import auth_blueprint
    from app.main.search.views import search_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(search_blueprint, url_prefix='/search')

    return app
