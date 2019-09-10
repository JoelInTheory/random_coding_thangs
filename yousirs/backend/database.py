# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

app_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(app_dir, 'data/you_sirs.db')

engine = create_engine('sqlite:///%s' % db_file, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
