import psycopg2
from psycopg2.pool import PersistentConnectionPool
from settings import Config
import threading

pool = PersistentConnectionPool(5,200, user='admin', password = 'admin8653', dbname = 'Api', host="192.168.1.41", port="5432")



from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://admin:admin8653@127.0.0.1:5432/Api', pool_size=100, pool_recycle=5, pool_timeout=180, pool_pre_ping=True, max_overflow=0)

session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = session.query_property()