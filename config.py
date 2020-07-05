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
    ELASTICSEARCH_URL = 'https://search-bloganuong-es2-6dzkl36ttjgctbjass26vku7qu.ap-southeast-1.es.amazonaws.com'

    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_FILE_THRESHOLD = 100

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # MONGODB_DB = 'foodblog1'
    # MONGODB_HOST = 'mongodb+srv://hoangan:hoangan123456@cluster0-ypawj.gcp.mongodb.net/foodblog1?retryWrites=true&w=majority'
    MONGODB_DB = 'foodblog_opt1'
    MONGODB_HOST = 'mongodb+srv://admin:britcat@clusteroptimize-wysnm.gcp.mongodb.net/foodblog_opt1?retryWrites=true&w=majority'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True
    MONGODB_DB = 'test_blogfood_2'
    MONGODB_HOST = 'mongodb://localhost:27017/test_blogfood_2'
    ELASTICSEARCH_URL = 'http://localhost:9200'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
