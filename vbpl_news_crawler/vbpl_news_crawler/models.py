from sqlalchemy import *
from sqlalchemy.engine.url import URL 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime
import settings
import time
import datetime

DeclarativeBase = declarative_base()

def db_connect():
	return create_engine(URL(**settings.DATABASE))
def create_news_table(engine):
	DeclarativeBase.metadata.create_all(engine)
class News(DeclarativeBase):
	__tablename__ = "news"
	doc_id = Column('doc_id',String,primary_key=True)
	title = Column('title',String)
	url = Column('url',String)
	description = Column('description',String)
	content = Column('content',String)
	public_date = Column('public_date',String)
	created_at = Column('created_at',String)
	updated_at = Column('updated_at',String)
