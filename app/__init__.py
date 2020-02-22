from flask import Flask
from flask_mongoengine import MongoEngine
from elasticsearch import Elasticsearch
from config import config
# from app.cache import cache
from flask_bcrypt import Bcrypt
from flask_session import Session

db = MongoEngine()
bcrypt = Bcrypt()
sess = Session()


def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    bcrypt.init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    # cache.init_app(app)
    sess.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.main.auth.views import auth_blueprint
    from app.main.search.views import search_blueprint
    from app.main.store.views import store_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(search_blueprint, url_prefix='/search')
    app.register_blueprint(store_blueprint, url_prefix='/')

    return app
