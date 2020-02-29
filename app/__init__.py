from flask import Flask
from flask_mongoengine import MongoEngine
from elasticsearch import Elasticsearch

from app.decorators import async_func
from config import config
# from app.cache import cache
from flask_bcrypt import Bcrypt
from flask_session import Session

db = MongoEngine()
bcrypt = Bcrypt()
sess = Session()


def create_app(config_name):
    app = Flask(__name__)

    bcrypt.init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    # cache.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    sess.init_app(app)


    from app.main.auth.views import auth_blueprint
    from app.main.search.views import search_blueprint
    from app.main.store.views import store_blueprint
    from app.main.user.views import user_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(search_blueprint, url_prefix='/search')
    app.register_blueprint(store_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/profile')

    return app
