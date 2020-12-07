from typing import List, Optional
from .models import VirtualMachine, User
from pydantic import BaseModel, Field
import random


class VirtualMachineSchema(BaseModel):
    id: Optional[str] = Field(None, example=123)
    name: str = Field(f'vm-{random.randint(1, 9999)}', example='vm-name')
    description: str = Field('no-description', example='some-description')
    cpu: int = Field(1, example=1)
    ram: int = Field(1024, example=1024)
    hdd: int = Field(1024, example=1024)
    owner: int = Field(1, example=1)

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
