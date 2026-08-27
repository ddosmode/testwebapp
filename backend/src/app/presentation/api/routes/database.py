from fastapi import APIRouter

from app.infrastructure.database import Base

router = APIRouter(tags=["database"])


@router.get("/database")
async def database() -> dict[str, object]:
    return {
        "status": "ok",
        "tables": sorted(Base.metadata.tables.keys()),
    }
