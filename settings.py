import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = os.getenv('FK_DEBUG', True)
# DONOT use in docker deployment
#    SERVER_NAME   = '{}:{}'.format(os.getenv('FK_HOST', '127.0.0.1'), os.getenv('FK_PORT', 5000))
#    SERVER_NAME   = '{}:5000'.format(os.getenv('FK_HOST', '127.0.0.1'))
    JSON_AS_ASCII = False
    SECRET_KEY    = 'BwcKCQMEDwAEDgsCBAkICw'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_REQUIRED = os.getenv('FK_JWT_TOKEN', False)
    AUTH_USER     = os.getenv('FK_TOKEN_USER', 'kfsyscc')
    AUTH_PASSWORD = os.getenv('FK_TOKEN_PASSWORD', 'app1858')
    AUTH_EXPIRED  = 15 #MINS

    ORA_DSN = os.getenv('FK_ORA_TNSNAME', 'TEST').upper()
    ORA_USER = os.getenv('FK_ORA_USER', 'kfsyscc')
    ORA_PASSWORD = os.getenv('FK_ORA_PASSWORD', 'app1858')
    ORA_SESSION_IDLE_TIMEOUT = 90 #secs

    PG_USER = os.getenv('FK_PG_USER', 'admin')
    PG_POSSWORD = os.getenv('FK_PG_POSSWORD', 'admin8653')
    PG_SERVER = os.getenv('FK_PG_SERVER', '192.168.1.41')
    PG_POART = os.getenv('FK_PG_POART', '5432')
    PG_DB = os.getenv('FK_PG_DB', 'Api')

    PG_CONNECTION_STRING = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(PG_USER, PG_POSSWORD, PG_SERVER, PG_POART, PG_DB)
    #'postgresql+psycopg2://' + PG_USER+ ':' + PG_POSSWORD + '@' + PG_SERVER+ ':'+PG_POART+ '/' +  PG_DB



    LOG_DIR =  os.path.join(basedir, 'log')
    LOG_FILENAME =  'Server.log'
    LOG_URI =  LOG_DIR + '/' + LOG_FILENAME


class Message(object):
    TOKEN_IS_MISING = 'Access token is missing in the authorization http request head.'