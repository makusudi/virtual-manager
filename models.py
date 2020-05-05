import asyncio
from gino import Gino
from config import CONNECTION_STRING


database = Gino()


class DBException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Users(database.Model):
    '''Model for user'''
    __tablename__ = 'users'

    id = database.Column(database.Integer(), primary_key=True)
    name = database.Column(database.String(), nullable=False)
    last_name = database.Column(database.String(), nullable=False)
    password = database.Column(database.String(), nullable=False)
    vms = database.Column(database.JSON)
    dbs = database.Column(database.JSON)

    @staticmethod
    async def get_by_name(name: str):
        async with database.with_bind(CONNECTION_STRING):
            user = await Users.query.where(Users.name == name).gino.first()
        return user

    @staticmethod
    async def new(name: str, last_name: str, password: str):
        async with database.with_bind(CONNECTION_STRING):
            user = await Users.create(name=name, last_name=last_name, password=password, vms=[], dbs=[])
        return user

    async def update_values(self, **kwargs):
        for attr in kwargs:
            if not getattr(self, attr, None):
                raise DBException(message="invalid attribute")
        async with database.with_bind(CONNECTION_STRING):
            new_rec = await self.update(**kwargs).apply()
        return new_rec

    async def delete_user(self):
        async with database.with_bind(CONNECTION_STRING):
            await self.delete()

    async def to_dict(self):
        return {'name': self.name, 'last_name': self.last_name}


class VM(database.Model):
    '''Model for virtual machine'''
    __tablename__ = 'vm'

    id = database.Column(database.Integer(), primary_key=True)
    name = database.Column(database.String(), nullable=False, unique=True)
    description = database.Column(database.String())
    cpu = database.Column(database.Integer(), nullable=False)
    ram = database.Column(database.Integer(), nullable=False)
    hdd = database.Column(database.Integer(), nullable=False)
    owner = database.Column(database.Integer(), database.ForeignKey('users.id'), nullable=False)

    @staticmethod
    async def new(name: str, description: str, cpu: int, ram: int, hdd: int, owner: int):
        exists = await VM.get_by_name(name)
        if exists:
            raise DBException(message='please provide another vm name')
        async with database.with_bind(CONNECTION_STRING):
            new_rec = await VM.create(name=name, description=description, cpu=cpu, ram=ram, hdd=hdd, owner=owner)
        return new_rec

    @staticmethod
    async def get_by_name(name: str):
        async with database.with_bind(CONNECTION_STRING):
            vm = await VM.query.where(VM.name == name).gino.first()
        return vm if vm else None

    @staticmethod
    async def get_by_owner(owner_id: int):
        async with database.with_bind(CONNECTION_STRING):
            vms = await VM.query.where(VM.owner == owner_id).gino.all()
        return vms

    async def update_values(self, **kwargs):
        for attr in kwargs:
            if not getattr(self, attr, None):
                raise DBException(message=f"Invalid attribute {attr}")
        async with database.with_bind(CONNECTION_STRING):
            new_rec = await self.update(**kwargs).apply()
        return new_rec

    async def delete_vm(self):
        async with database.with_bind(CONNECTION_STRING):
            await self.delete()

    async def to_dict(self):
        return {'name': self.name, 'description': self.description, 'cpu': self.cpu,
                'hdd': self.hdd, 'ram': self.ram, 'owner': self.owner}


async def drop_all():
    async with database.with_bind(CONNECTION_STRING):
        await database.gino.drop_all()


async def create_all():
    import random
    async with database.with_bind(CONNECTION_STRING):
        await database.gino.create_all()
    await Users.new(name='admin', last_name='admin', password='admin')
    lorem = 'Lorem ipsum dolor sit amet consectetur adipiscing'
    for x in range(9):
        print(f'Creating VM # {x}')
        desc = ''
        splitted = lorem.split(' ')
        for index in range(random.randint(1, 3)):
            desc += (splitted[index] + ' ')
        await VM.new(
            name=f'test_vm_{x}',
            description=desc,
            cpu=random.randint(1, 16),
            ram=random.randint(1, 8)*4,
            hdd=random.randint(32, 512),
            owner=1
        )


if __name__ == '__main__':
    asyncio.run(create_all())
