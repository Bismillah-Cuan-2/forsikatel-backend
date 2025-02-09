from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

db_username = os.getenv("DEV_DB_USERNAME")
db_password = os.getenv("DEV_DB_PASSWORD")
db_host = os.getenv("DEV_DB_HOST")
db_port = os.getenv("DEV_DB_PORT")
db_name = os.getenv("DEV_DB_NAME")

DB_URI = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DB_URI)

connection = engine.connect()
print("connected to db")

Session = sessionmaker(connection)