# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

DB_URL = os.environ("DATABASE_URL")
engine = create_engine(DB_URL, pool_size=10)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models # noqa
