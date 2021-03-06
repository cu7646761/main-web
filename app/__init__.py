from flask import Flask
from flask_mongoengine import MongoEngine
from elasticsearch import Elasticsearch

# from app.cache import cache
from app.decorators import async_func
from config import config
from flask_bcrypt import Bcrypt
from flask_session import Session
import time
from flask import g

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
    from app.main.analyze_sentiment.views import analyze_blueprint
    from app.main.user.views import user_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(search_blueprint, url_prefix='/search')
    app.register_blueprint(store_blueprint, url_prefix='/')
    app.register_blueprint(analyze_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/profile')

    from app.admin.auth.views import auth_admin_blueprint
    app.register_blueprint(auth_admin_blueprint, url_prefix='/admin')

    from app.admin.store.views import store_admin_blueprint
    app.register_blueprint(store_admin_blueprint, url_prefix='/admin/store')
    from app.admin.user.views import user_admin_blueprint
    app.register_blueprint(user_admin_blueprint, url_prefix='/admin/user-management')

    if config_name != 'testing':
        @app.before_request
        def before_request():
            g.start = time.time()

        @app.after_request
        def after_request(response):
            diff = time.time() - g.start
            if ((response.response) and
                    (200 <= response.status_code < 300) and
                    (response.content_type.startswith('text/html'))):
                print("Time duration: ", diff)
                response.set_data(response.get_data().replace(
                    b'__EXECUTION_TIME__', bytes(str(diff), 'utf-8')))
            return response

    return app
