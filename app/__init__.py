from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from elasticsearch import Elasticsearch
from config import config

from app.cache import cache

db = MongoEngine()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    cache.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.main.user.views import user_blueprint
    from app.main.home.views import home_blueprint

    from app.CRUD.city.views import city_blueprint
    from app.CRUD.district.views import district_blueprint
    from app.CRUD.address.views import address_blueprint
    from app.main.search.views import search_blueprint

    app.register_blueprint(user_blueprint, url_prefix='/')
    app.register_blueprint(home_blueprint, url_prefix='/')

    app.register_blueprint(city_blueprint, url_prefix='/city')
    app.register_blueprint(district_blueprint, url_prefix='/district')
    app.register_blueprint(address_blueprint, url_prefix='/address')
    app.register_blueprint(search_blueprint, url_prefix='/search')

    return app
