from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types, Column,String


Base = declarative_base()


class DemoData():
    def __init__(self,config):
        engine = create_engine(config.database_connection, echo=False)
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        Session = sessionmaker(bind=engine)
        self.session = Session()


class Instance(Base):
    __tablename__ = 'instance'
    id = Column(types.Integer, primary_key=True)
    openstack_id = Column(String(255), unique=True)
    name = Column(String(255))
    status = Column(String(255), nullable=False)
    launched_at = Column(types.DATETIME)
    life_time = Column(types.Integer, nullable=False)