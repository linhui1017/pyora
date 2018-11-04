import datetime
from sqlalchemy import Column, String, Integer, DateTime

from db.database import pg_Base


class LineProfile(pg_Base):
    __tablename__ = 'LINE_PROFILE'

    USER_ID = Column(String, primary_key=True)
    USER_NAME = Column(String)
    LAST_UPDATE_TIME = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, userid, username):
        self.USER_ID = userid
        self.USER_NAME = userid


