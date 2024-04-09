from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_tools.db_tools import Asset
from variables import USERNAME, PASSWORD, HOST, PORT, DATABASE, PAIRS

# Creating a connection to the database
engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
Session = sessionmaker(bind=engine)
session = Session()

# Filling out the Assets table
for pair in PAIRS:
    asset = Asset(pair=pair)
    session.add(asset)

session.commit()
