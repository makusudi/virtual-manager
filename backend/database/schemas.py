from typing import List
from .models import VirtualMachine, User
from pydantic import BaseModel


class VirtualMachineSchema(BaseModel):
    id: int
    name: str
    description: str
    cpu: int
    ram: int
    hdd: int
    owner: int

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    name: str
    last_name: str
    vms: List[VirtualMachineSchema]
    dbs: List = []

    class Config:
        orm_mode = True


UserSchema.update_forward_refs()
VirtualMachineSchema.update_forward_refs()
