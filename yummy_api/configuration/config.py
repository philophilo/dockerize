import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent configurations"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this is the secrete'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class StagingConfig(Config):
    """staging configuration"""
    DEVELOPMENT = True
    DEBUG = True


class DevelopingConfig(Config):
    """Developement configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                             "postgresql://philophilo:philophilo@localhost/yummy")
    DEVELOPING = True
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                             "postgresql://localhost/test_yummy")
    TESTING = True


class LocalTestingConfig(Config):
    """Local testing configuration"""
    SQLALCHEMY_DATABASE_URI = "postgresql://philophilo:philophilo@localhost/test_yummy"
    TESTING = True
