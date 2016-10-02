from sqlalchemy import Column, Integer, String, DateTime, BINARY
import datetime
from . import Base


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    token = Column(BINARY(64), nullable=False, unique=True)
    path = Column(String(512), nullable=False)
    data_type = Column(String(50), default='binary')
    at_created = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, name, token, path, data_type):
        self.name = name
        self.token = token
        self.path = path
        self.data_type = data_type

    def __repr__(self):
        return 'Data(name={0}, token={1}, path={2}, data_type={3})'.format(
            self.name, self.token, self.path, self.data_type)
