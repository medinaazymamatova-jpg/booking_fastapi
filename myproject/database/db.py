from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base


DB_URl = 'sqlite:///./database.db'

engine = create_engine(DB_URl)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
     pass