from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    name = Column(String(50))
    password = Column(String(80))
    admin = Column(Boolean)
    
    def __repr__(self):
        return '<User %r>' % (self.name)
