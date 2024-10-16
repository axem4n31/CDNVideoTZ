from typing import List
import httpx
from sqlalchemy import select, and_, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from math import radians, cos, sin, sqrt, atan2

from starlette import status
from starlette.responses import JSONResponse

from app import settings
from models.model import City
from models.schemas import CitySchema


async def get_city_coordinates(name_city: str) -> CitySchema | None:
    url = settings.WEATHER_API + "search.json"
    url += "?key=" + settings.WEATHER_API_TOKEN
    url += f"&q={name_city}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
        message = response.json()
        if not message:
            return

        return CitySchema(
            name_city=message[0]["name"], lat=message[0]["lat"], lon=message[0]["lon"]
        )

    except httpx.TimeoutException as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except Exception as e:
        print(f"Error get_city_coordinates : {e}")


async def add_city(city_data: CitySchema, db: AsyncSession) -> JSONResponse:
    try:
        city = City(lat=city_data.lat, lon=city_data.lon, name_city=city_data.name_city)
        db.add(city)
        await db.commit()
        return JSONResponse(
            content={"message": "Город успешно добавлен."},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        print(f"Error add_city : {e}")


def haversine(lat1, lon1, lat2, lon2):
    earth_radius = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = earth_radius * c
    return distance


async def get_city_data(
    lat: float, lon: float, db: AsyncSession
) -> List[CitySchema] | None:

    city = await db.scalar(select(City).where(and_(City.lat == lat, City.lon == lon)))
    if city:
        return [CitySchema(lat=city.lat, lon=city.lon, name_city=city.name_city)]
    city_alias = aliased(City)
    closest_cities = await db.execute(
        select(
            city_alias,
            (
                func.pow(func.sin(func.radians(city_alias.lat - lat) / 2), 2)
                + func.cos(func.radians(lat))
                * func.cos(func.radians(city_alias.lat))
                * func.pow(func.sin(func.radians(city_alias.lon - lon) / 2), 2)
            ).label("distance"),
        )
        .order_by("distance")
        .limit(2)
    )

    city_list = [
        CitySchema(lat=city.lat, lon=city.lon, name_city=city.name_city)
        for city, _ in closest_cities.all()
    ]

    return city_list if city_list else None


async def delete_city_by_name(name_city: str, db: AsyncSession) -> None:
    city = delete(City).where(City.name_city == name_city)
    await db.execute(city)
    await db.commit()


async def get_city_data_by_name(name_city: str, db: AsyncSession) -> CitySchema:
    city = await db.scalar(select(City).where(and_(City.name_city == name_city)))
    if city:
        return CitySchema(lat=city.lat, lon=city.lon, name_city=city.name_city)
