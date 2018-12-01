from sqlalchemy import create_engine, Column, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base

# Connecting to a HEROKU postgresql
engine = create_engine('your url', echo=True)

# Creating a base class
Base = declarative_base()


# Creating a table class
class Members(Base):
    __tablename__ = 'members'

    tab_id = Column(Integer, primary_key=True, nullable=False)
    vk_id = Column(Integer, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    sex = Column(Integer, nullable=False)
    photo_link = Column(Text, nullable=False)
    rating = Column(Float, nullable=False, default=0.0)

# Creating an actual table
Base.metadata.create_all(engine)