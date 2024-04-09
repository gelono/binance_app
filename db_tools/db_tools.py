from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

from time_measure.time_measure import measure_time
from variables import USERNAME, PASSWORD, HOST, PORT, DATABASE

Base = declarative_base()


class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    pair = Column(String, unique=True)

    records = relationship('VolumeRecord', back_populates='asset')


class VolumeRecord(Base):
    __tablename__ = 'volume_records'

    id = Column(Integer, primary_key=True)
    pair_id = Column(Integer, ForeignKey('assets.id'))
    timestamp = Column(DateTime(timezone=True))
    total_ask_volume = Column(Float)
    total_bid_volume = Column(Float)

    asset = relationship('Asset', back_populates='records')


@measure_time
async def write_volume(pair, timestamp, ask_volume, bid_volume):
    """
    Asynchronous function to write volume data to the database.

    Args:
        pair (str): The trading pair for which the volume data is recorded.
        timestamp (datetime): The timestamp of the volume data.
        ask_volume (float): The total ask volume to be recorded.
        bid_volume (float): The total bid volume to be recorded.

    Returns:
        None

    """

    engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
    Session = sessionmaker(bind=engine)
    session = Session()

    asset = session.query(Asset).filter_by(pair=pair).first()
    if not asset:
        asset = Asset(pair=pair)
        session.add(asset)
        session.commit()

    volume_record = VolumeRecord(
        pair_id=asset.id,
        timestamp=timestamp,
        total_ask_volume=ask_volume,
        total_bid_volume=bid_volume
    )

    session.add(volume_record)
    session.commit()
