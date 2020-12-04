from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import CONNECTION_STRING


engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
session = Session()


class DBException(Exception):
    def __init__(self, message):
        super().__init__(message)


class VM(Base):
    '''Model for virtual machine'''
    __tablename__ = 'vm'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    cpu = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)
    hdd = Column(Integer, nullable=False)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    @staticmethod
    def new(name: str, description: str, cpu: int, ram: int, hdd: int, owner: int):
        exists = VM.get_by_name(name)
        if exists:
            raise DBException(message='please provide another vm name')
        new_rec = VM(name=name, description=description, cpu=cpu, ram=ram, hdd=hdd, owner=owner)
        session.add(new_rec)
        session.commit()
        return new_rec

    @staticmethod
    def get_by_name(name: str):
        vm = session.query(VM).filter(VM.name == name).first()
        return vm if vm else None

    @staticmethod
    def get_by_owner(owner_id: int):
        vms = session.query(VM).filter(VM.owner == owner_id).all()
        return vms

    def update_values(self, **kwargs):
        for attr in kwargs:
            if not getattr(self, attr, None):
                raise DBException(message=f"Invalid attribute {attr}")
        needed = session.query(self).filter(**kwargs).first()
        for key, value in kwargs.items():
          setattr(needed, key, value)
        session.add(needed)
        session.commit()
        return needed

    def delete_vm(self):
        needed = session.query(self).first()
        session.delete(needed)
        session.commit()
        return needed

    def to_dict(self):
        return {'name': self.name, 'description': self.description, 'cpu': self.cpu,
                'hdd': self.hdd, 'ram': self.ram, 'owner': self.owner}

res = VM.get_by_name('test_vm_0')
print(res)
