from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class InventoryUnitModel(Base):
    __tablename__ = "inventory_units"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
