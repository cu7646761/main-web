import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SECRET_KEY = 'hard to guess string'
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

    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=5)
    # The maximum number of items the session stores
    # before it starts deleting some, default 500
    SESSION_FILE_THRESHOLD = 100

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DB = 'foodblog1'
    MONGODB_HOST = 'mongodb+srv://hoangan:hoangan123456@cluster0-ypawj.gcp.mongodb.net/foodblog1?retryWrites=true&w=majority'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True
    MONGODB_DB = 'main_3'
    MONGODB_HOST = 'mongodb://localhost:27017/main_3'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
