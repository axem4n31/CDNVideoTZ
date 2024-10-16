from models.model_settings import Base
from sqlalchemy import Column, Integer, String, Float


class City(Base):
    __tablename__ = "City"
    id_city = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    name_city = Column(String)
