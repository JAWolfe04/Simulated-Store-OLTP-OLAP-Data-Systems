from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from apis.business_api import settings

engine = create_engine(settings.POSTGRES_DB_CONN)

SessionLocal = sessionmaker(autocommit = False, autoflush = False,
                            bind = engine)

Base = declarative_base()
