from fastapi import APIRouter

from app.infrastructure.database.session import engine

router = APIRouter(tags=["database"])


@router.get("/health/database")
async def database_health() -> dict[str, str]:
    try:
        async with engine.connect() as connection:
            result = await connection.exec_driver_sql("SELECT 1")
            if result.scalar_one() != 1:
                raise RuntimeError("database health check returned unexpected result")
        return {"status": "ok"}
    except Exception:
        return {"status": "error"}
