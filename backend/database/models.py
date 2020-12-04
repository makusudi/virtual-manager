from typing import List, Union
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import CONNECTION_STRING


engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
session = Session()


class DBException(Exception):
    def __init__(self, message):
        super().__init__(message)


class User(Base):
    '''Model for user'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    vms = Column(JSON)
    dbs = Column(JSON)

    @staticmethod
    def get_by_name(name: str) -> 'User':
        user = session.query(User).filter(User.name == name).first()
        return user

    @staticmethod
    def new(name: str, last_name: str, password: str) -> 'User':
        user = User(name=name, last_name=last_name, password=password, vms=[], dbs=[])
        session.add(user)
        session.commit()
        return user

    def update(self, **kwargs) -> 'User':
        for attr in kwargs:
            if not getattr(self, attr, None):
                raise DBException(message="invalid attribute")
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.add(self)
        session.commit()
        return self

    def delete(self) -> 'User':
        session.delete(self)
        session.commit()
        return self

    def to_dict(self) -> dict:
        return {'name': self.name, 'last_name': self.last_name}


class VirtualMachine(Base):
    '''Model for virtual machine'''
    __tablename__ = 'vms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    cpu = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)
    hdd = Column(Integer, nullable=False)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    @staticmethod
    def list() -> List['VirtualMachine']:
        return session.query(VirtualMachine).all()

    @staticmethod
    def new(name: str, description: str, cpu: int, ram: int, hdd: int, owner: int) -> 'VirtualMachine':
        exists = VirtualMachine.get_by_name(name)
        if exists:
            raise DBException(message='please provide another vm name')
        new_rec = VirtualMachine(name=name, description=description, cpu=cpu, ram=ram, hdd=hdd, owner=owner)
        session.add(new_rec)
        session.commit()
        return new_rec

    @staticmethod
    def get_by_name(name: str) -> Union['VirtualMachine', None]:
        vm = session.query(VirtualMachine).filter(VirtualMachine.name == name).first()
        return vm if vm else None

    @staticmethod
    def get_by_owner(owner_id: int) -> List['VirtualMachine']:
        vms = session.query(VirtualMachine).filter(VirtualMachine.owner == owner_id).all()
        return vms

    def update(self, **kwargs) -> 'VirtualMachine':
        for attr in kwargs:
            if not getattr(self, attr, None):
                raise DBException(message=f"Invalid attribute {attr}")
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.add(self)
        session.commit()
        return self

    def delete(self) -> 'VirtualMachine':
        session.delete(self)
        session.commit()
        return self

    def to_dict(self) -> dict:
        return {'name': self.name, 'description': self.description, 'cpu': self.cpu,
                'hdd': self.hdd, 'ram': self.ram, 'owner': self.owner}


def drop_all():
    Base.metadata.drop_all(bind=engine)


def create_all():
    Base.metadata.create_all(bind=engine)
    User.new('admin', 'admin', 'admin')

    for i in range(9):
        VirtualMachine.new(
          name=f'test_{i+1}',
          description=f'description_{i+2}',
          cpu=i,
          ram=i,
          hdd=64 * i,
          owner=1
        )


if __name__ == '__main__':
    create_all()
