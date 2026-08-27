from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.infrastructure.database.session import SessionFactory
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("")
async def get_cart() -> dict[str, object]:
    return {"items": [], "total": "0.00", "currency": "EUR"}


@router.post("/items")
async def add_to_cart(product_id: UUID, quantity: int = 1) -> dict[str, object]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        product = await uow.products.get(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

    return {
        "product_id": str(product_id),
        "quantity": quantity,
        "unit_price": str(product.price),
        "currency": getattr(product, "currency", "EUR"),
    }


@router.delete("/items/{item_id}")
async def remove_from_cart(item_id: UUID) -> dict[str, object]:
    return {"removed": str(item_id)}


@router.delete("")
async def clear_cart() -> dict[str, object]:
    return {"cleared": True}
