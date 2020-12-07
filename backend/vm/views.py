from typing import List, Optional
from fastapi import FastAPI, HTTPException
from database import VirtualMachineSchema, VirtualMachine, User

vm_app = FastAPI()


@vm_app.get('/', response_model=List[VirtualMachineSchema])
def get_vms(owner: Optional[str] = None):
    if not owner:
        return VirtualMachine.list()

    user: User = User.get_by_name(owner)
    return VirtualMachine.get_by_owner(user.id) if user else []


@vm_app.post('/', response_model=VirtualMachineSchema)
def create_vm(vm: VirtualMachineSchema):
    data: dict = vm.dict()
    new_vm: VirtualMachine = VirtualMachine.new(
      data['name'],
      data['description'],
      data['cpu'],
      data['ram'],
      data['hdd'],
      data['owner']
    )
    return new_vm.to_dict()


@vm_app.put('/', response_model=VirtualMachineSchema)
def change_vm(vm: VirtualMachineSchema):
    data: dict = vm.dict()
    exists: VirtualMachine = VirtualMachine.get_by_name(data['name'])
    if not exists:
        raise HTTPException(status_code=404, detail='not found')

    res = exists.update(**{k: v for k, v in data.items() if k != 'id'})
    return res


@vm_app.delete('/', response_model=VirtualMachineSchema)
def delete_vm(vm: VirtualMachineSchema):
    data: dict = vm.dict()
    exists: VirtualMachine = VirtualMachine.get_by_name(data['name'])
    if not exists:
        raise HTTPException(status_code=404, detail='not found')

    exists.delete()
    return exists
