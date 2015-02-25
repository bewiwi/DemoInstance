from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types, Column, String
import uuid

Base = declarative_base()


class DemoData():
    session = None

    @staticmethod
    def get_session(config):
        if DemoData.session is not None:
            return DemoData.session
        engine = create_engine(config.database_connection, echo=False)
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        Session = sessionmaker(
            bind=engine, autocommit=False,
            autoflush=True, expire_on_commit=True
        )
        DemoData.session = Session()
        return DemoData.session


class Instance(Base):
    __tablename__ = 'instance'
    id = Column(types.Integer, primary_key=True)
    openstack_id = Column(String(255), unique=True)
    name = Column(String(255))
    image_key = Column(String(255))
    status = Column(String(255), nullable=False)
    launched_at = Column(types.DATETIME)
    life_time = Column(types.Integer, nullable=False)
    token = Column(String(255), nullable=False)


class User(Base):
    __tablename__ = 'user'
    token = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True)
    last_connection = Column(types.DATETIME)

    def generate_token(self):
        self.token = str(uuid.uuid4())
        return self.token
