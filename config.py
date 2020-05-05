import os

DB_HOST = os.environ.get('DB_HOST')
DB_USER = 'postgres'
DB_PASS = 'postgres'
CONNECTION_STRING = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/postgres'
