from pydantic import BaseModel


class CitySchema(BaseModel):
    name_city: str | None
    lat: float
    lon: float
