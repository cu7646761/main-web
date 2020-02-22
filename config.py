import os
import redis
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'fcache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_URL = 'redis://localhost:6379'
    DEBUG_TB_PANELS = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_mongoengine.panels.MongoDebugPanel'
    )
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    ELASTICSEARCH_URL = 'http://localhost:9200'

    # Flask-Session
    # SESSION_TYPE = environ.get('SESSION_TYPE')
    # SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))
    SESSION_TYPE = redis
    # redis: //:[password] @ [host_url]: [port]
    SESSION_REDIS = "redis://localhost:6379"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DB = 'main_1'
    MONGODB_HOST = 'mongodb://localhost:27017/main_1'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True
    MONGODB_DB = 'main_1'
    MONGODB_HOST = 'mongodb://localhost:27017/main_1'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
