from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.infrastructure.database.session import SessionFactory
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("")
async def list_cities() -> list[dict[str, object]]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        cities = await uow.cities.list_active()

    return [
        {
            "id": str(city.id),
            "name": city.name,
            "is_active": city.is_active,
        }
        for city in cities
    ]


@router.get("/{city_id}")
async def get_city(city_id: UUID) -> dict[str, object]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        city = await uow.cities.get(city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return {
        "id": str(city.id),
        "name": city.name,
        "is_active": city.is_active,
    }


@router.get("/{city_id}/locations")
async def list_locations(city_id: UUID) -> list[dict[str, object]]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        locations = await uow.locations.list_by_city(city_id)

    return [
        {
            "id": str(location.id),
            "city_id": str(location.city_id),
            "name": location.name,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "is_active": location.is_active,
        }
        for location in locations
    ]
