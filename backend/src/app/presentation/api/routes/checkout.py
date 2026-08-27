from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.application.orders.services import OrderService
from app.domain.orders.entities import Order, OrderItem
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork

router = APIRouter(prefix="/checkout", tags=["checkout"])


@router.post("")
async def checkout(
    user_id: UUID,
    city_id: UUID | None = None,
    payment_method_id: UUID | None = None,
) -> dict[str, object]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        user = await uow.users.get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

    order = Order(
        id=UUID("00000000-0000-0000-0000-000000000000"),
        user_id=user_id,
        total=0,
        currency="EUR",
    )

    service = OrderService(SqlAlchemyUnitOfWork(SessionFactory))
    await service.create_order(order, [])

    return {
        "order_id": str(order.id),
        "status": order.status,
        "total": str(order.total),
        "currency": order.currency,
    }
