import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = "31a9245b90d7eb56bdd16063fe668bb1e9f663cfeb65765884784bef"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dbs/dev.db'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
