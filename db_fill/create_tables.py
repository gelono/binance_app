from sqlalchemy import create_engine
from variables import USERNAME, PASSWORD, HOST, PORT, DATABASE
from db_tools.db_tools import Base


# Creating a connection to the database
engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

# Creating tables
Base.metadata.create_all(engine)
