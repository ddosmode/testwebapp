from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.application.orders.services import OrderService
from app.domain.orders.entities import Order, OrderItem
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork

router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_service() -> OrderService:
    return OrderService(SqlAlchemyUnitOfWork(SessionFactory))


@router.get("")
async def list_orders(user_id: UUID | None = None) -> list[dict[str, object]]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        if user_id is not None:
            orders = await uow.orders.list_by_user(user_id)
        else:
            orders = await uow.orders.list()

    return [
        {
            "id": str(order.id),
            "user_id": str(order.user_id),
            "total": str(order.total),
            "currency": getattr(order, "currency", "EUR"),
            "status": order.status,
            "created_at": order.created_at.isoformat() if order.created_at else None,
        }
        for order in orders
    ]


@router.get("/{order_id}")
async def get_order(order_id: UUID) -> dict[str, object]:
    service = get_order_service()

    try:
        order = await service.get_order(order_id)
    except Exception as exc:
        if exc.__class__.__name__ == "EntityNotFoundError":
            raise HTTPException(status_code=404, detail="Order not found") from exc
        raise

    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        items = await uow.order_items.list_by_order(order_id)

    return {
        "id": str(order.id),
        "user_id": str(order.user_id),
        "total": str(order.total),
        "currency": getattr(order, "currency", "EUR"),
        "status": order.status,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "items": [
            {
                "id": str(item.id),
                "order_id": str(item.order_id),
                "product_id": str(item.product_id),
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
            }
            for item in items
        ],
    }


@router.post("")
async def create_order(order: Order, items: list[OrderItem] | None = None) -> dict[str, object]:
    service = get_order_service()
    await service.create_order(order, items or [])
    return {"id": str(order.id)}
