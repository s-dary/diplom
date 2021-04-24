from os.path import join, abspath, dirname

basedir = abspath(dirname(__file__))


class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'app.db')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Config WTF
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    # security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
