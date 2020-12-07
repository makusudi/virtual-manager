from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vm import vm_app


app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


app.mount('/api/vm', vm_app)


@app.get('/')
def frontend():
    pass
