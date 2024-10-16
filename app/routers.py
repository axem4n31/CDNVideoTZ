from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.service import (
    get_city_coordinates,
    add_city,
    get_city_data,
    delete_city_by_name,
    get_city_data_by_name,
)
from models.model_settings import db_helper

app_router = APIRouter(prefix="/app", tags=["app"])


@app_router.get("/get_city")
async def get_city_router(
    lat: float = None,
    lon: float = None,
    name_city: str = None,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if name_city is not None:
        city_data = await get_city_data_by_name(name_city=name_city, db=db)
        if city_data:
            return city_data
        raise HTTPException(status_code=404, detail="Город не найден.")
    if lat is not None and lon is not None:
        city_data = await get_city_data(lat=lat, lon=lon, db=db)
        if city_data:
            return city_data
        raise HTTPException(status_code=404, detail="Город по координатам не найден.")
    raise HTTPException(
        status_code=400,
        detail="Необходимо передать либо 'lat' и 'lon', либо 'name_city'.",
    )


@app_router.post("/add_city")
async def add_city_router(
    name_city: str, db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    city_data = await get_city_coordinates(name_city=name_city)
    if city_data is None:
        raise HTTPException(
            status_code=404,
            detail="Город не существует или координаты города отсутствуют.",
        )
    return await add_city(city_data=city_data, db=db)


@app_router.delete("/delete_city")
async def delete_city_router(
    name_city: str, db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await delete_city_by_name(name_city=name_city, db=db)
