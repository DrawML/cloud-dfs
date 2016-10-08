from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from cloud_dfs.database.db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME),
                       convert_unicode=True,  pool_recycle=1800)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import cloud_dfs.database.models
    Base.metadata.create_all(bind=engine)
