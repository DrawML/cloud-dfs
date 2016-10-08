from sqlalchemy import Column, Integer, String, DateTime, BINARY, ForeignKey
from sqlalchemy.orm import relationship, backref
import datetime
from cloud_dfs.database import Base


class DataGroup(Base):
    __tablename__ = 'data_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    token = Column(BINARY(64), nullable=False, unique=True)
    at_created = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, name, token):
        self.name = name
        self.token = token

    def __repr__(self):
        return 'DataGroup(name={0}, token={1}, len of data_list={2})'.format(
            self.name, self.token, len(self.data_list))


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    token = Column(BINARY(64), nullable=False, unique=True)
    fk_data_group = Column(Integer, ForeignKey('data_group.id'), nullable=True)
    path = Column(String(512), nullable=False)
    data_type = Column(String(50), default='binary')
    at_created = Column(DateTime, default=datetime.datetime.now)

    data_group = relationship(
        DataGroup,
        backref=backref('data_list',
                        uselist=True,
                        cascade='delete,all'))

    def __init__(self, name, token, path, data_type, data_group = None):
        self.name = name
        self.token = token
        self.path = path
        self.data_type = data_type
        self.data_group = data_group

    def __repr__(self):
        return 'Data(name={0}, token={1}, path={2}, data_type={3}, data_group.id={4})'.format(
            self.name, self.token, self.path, self.data_type, self.data_group.id if self.data_group else None)
