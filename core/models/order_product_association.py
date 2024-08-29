from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .product import Product
    from .order import Order

class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
            name="uniq_order_product_association",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    count: Mapped[int] = mapped_column(default=1, server_default='1')
    unit_price: Mapped[int] = mapped_column(default=0, server_default='0')

    order: Mapped['Order'] = relationship(back_populates='products_details')

    product: Mapped['Product'] = relationship(back_populates='orders_details')