from fastapi import APIRouter

from app.infrastructure.database.session import SessionFactory
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/methods")
async def list_payment_methods() -> list[dict[str, object]]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        methods = await uow.payment_methods.list_active()

    return [
        {
            "id": str(method.id),
            "name": method.name,
            "code": method.code,
            "is_active": method.is_active,
        }
        for method in methods
    ]
