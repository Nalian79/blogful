import os

class DevelopmentConfig(object):
#    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful"
    SQLALCHEMY_DATABASE_URI = "postgresql://:@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")

class TestingConfig(object):
#    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful-test"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/travis-ci-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
