
from settings import Config
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from lib.utils import to_dict, models_to_list

# Database of PostgreSQL
import psycopg2
#from psycopg2.pool import PersistentConnectionPool

pg_engine = create_engine(Config.PG_CONNECTION_STRING, pool_size=10, pool_recycle=3600, pool_timeout=180, pool_pre_ping=True, max_overflow=5, convert_unicode=True)
#engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
pg_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=pg_engine))
pg_Base = declarative_base()
pg_Base.query = pg_session.query_property() 
pg_Base.to_dict = to_dict   



