from pydantic import BaseModel


class VM(BaseModel):
    id: int
    name: str
    description: str
    cpu: int
    ram: int
    hdd: int
    owner: int
