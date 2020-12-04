from typing import List, Optional
from fastapi import FastAPI
from database import VirtualMachineSchema, VirtualMachine, User

vm_app = FastAPI()


@vm_app.get('/', response_model=List[VirtualMachineSchema])
def get_vms(owner: Optional[str] = None):
    if owner:
        user = User.get_by_name(owner)
        return VirtualMachine.get_by_owner(user.id) if user else []
    return VirtualMachine.list()
