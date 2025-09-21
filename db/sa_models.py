from sqlalchemy import MetaData, String, Text, BigInteger, Integer, Float, Numeric, TIMESTAMP, ForeignKey, \
    ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
})


class Base(DeclarativeBase):
    metadata = metadata


class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    external_order_id: Mapped[str | None] = mapped_column(Text)
    order_date_utc: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    last_updated_date_utc: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    deadline_date_utc: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    order_status: Mapped[str | None] = mapped_column(Text)
    invoice_status: Mapped[str | None] = mapped_column(Text)
    shipment_status: Mapped[str | None] = mapped_column(Text)
    shipping_total: Mapped[float | None] = mapped_column(Numeric(18, 4))
    sub_total: Mapped[float | None] = mapped_column(Numeric(18, 4))
    discount_total: Mapped[float | None] = mapped_column(Numeric(18, 4))
    order_total: Mapped[float | None] = mapped_column(Numeric(18, 4))
    currency_code: Mapped[str | None] = mapped_column(String(8))
    channel: Mapped[str | None] = mapped_column(Text)


class Customer(Base):
    __tablename__ = "customers"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True)
    internal_customer_id: Mapped[int | None] = mapped_column(BigInteger)
    user_id: Mapped[str | None] = mapped_column(Text)
    first_name: Mapped[str | None] = mapped_column(Text)
    last_name: Mapped[str | None] = mapped_column(Text)
    email_address: Mapped[str | None] = mapped_column(Text)


class Address(Base):
    __tablename__ = "addresses"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True)
    address_type: Mapped[str] = mapped_column(String(16), primary_key=True)  # 'billing' | 'shipping'
    id: Mapped[int | None] = mapped_column(BigInteger)
    external_address_id: Mapped[str | None] = mapped_column(Text)
    first_name: Mapped[str | None] = mapped_column(Text)
    last_name: Mapped[str | None] = mapped_column(Text)
    company_name: Mapped[str | None] = mapped_column(Text)
    address_line1: Mapped[str | None] = mapped_column(Text)
    address_line2: Mapped[str | None] = mapped_column(Text)
    address_line3: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(Text)
    state: Mapped[str | None] = mapped_column(Text)
    zip_code: Mapped[str | None] = mapped_column(Text)
    country_code: Mapped[str | None] = mapped_column(String(2))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)


class LineItem(Base):
    __tablename__ = "line_items"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True)
    line_item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sku: Mapped[str | None] = mapped_column(Text)
    product_name: Mapped[str | None] = mapped_column(Text)
    item_name: Mapped[str | None] = mapped_column(Text)
    quantity_ordered: Mapped[int | None] = mapped_column(Integer)
    quantity_invoiced: Mapped[int | None] = mapped_column(Integer)
    quantity_shipped: Mapped[int | None] = mapped_column(Integer)
    unit_price: Mapped[float | None] = mapped_column(Numeric(18, 4))
    unit_discount: Mapped[float | None] = mapped_column(Numeric(18, 4))
    sub_total: Mapped[float | None] = mapped_column(Numeric(18, 4))
    total_tax: Mapped[float | None] = mapped_column(Numeric(18, 4))
    total: Mapped[float | None] = mapped_column(Numeric(18, 4))


class LineItemTax(Base):
    __tablename__ = "line_item_taxes"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    line_item_id: Mapped[int] = mapped_column(primary_key=True)
    internal_tax_rate_id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float | None] = mapped_column(Numeric(18, 4))
    tax_type: Mapped[str | None] = mapped_column(Text)
    rate: Mapped[float | None] = mapped_column(Float)
    __table_args__ = (
        ForeignKeyConstraint(
            ["order_id", "line_item_id"],
            ["line_items.order_id", "line_items.line_item_id"],
            ondelete="CASCADE",
        ),
    )


class LineItemCustomField(Base):
    __tablename__ = "line_item_custom_fields"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    line_item_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (
        ForeignKeyConstraint(
            ["order_id", "line_item_id"],
            ["line_items.order_id", "line_items.line_item_id"],
            ondelete="CASCADE",
        ),
    )


# ---------- PAYMENTS ----------
class Payment(Base):
    __tablename__ = "payments"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True)
    order_payment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    payment_id: Mapped[int | None] = mapped_column(BigInteger)
    payment_type: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(Text)
    amount: Mapped[float | None] = mapped_column(Numeric(18, 4))
    amount_authorized: Mapped[float | None] = mapped_column(Numeric(18, 4))
    amount_captured: Mapped[float | None] = mapped_column(Numeric(18, 4))
    last_updated_by_staff_id: Mapped[int | None] = mapped_column(BigInteger)
    last_updated_by_staff_name: Mapped[str | None] = mapped_column(Text)


class PaymentCustomField(Base):
    __tablename__ = "payment_custom_fields"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    order_payment_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (
        ForeignKeyConstraint(
            ["order_id", "order_payment_id"],
            ["payments.order_id", "payments.order_payment_id"],
            ondelete="CASCADE",
        ),
    )


# ---------- SHIPPING ----------
class ShippingRate(Base):
    __tablename__ = "shipping_rates"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True)
    internal_shipping_rate_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    backend_name: Mapped[str | None] = mapped_column(Text)
    rate_code: Mapped[str | None] = mapped_column(Text)
    current_rate: Mapped[float | None] = mapped_column(Numeric(18, 4))


class ShippingTax(Base):
    __tablename__ = "shipping_taxes"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True)
    internal_tax_rate_id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float | None] = mapped_column(Numeric(18, 4))
    tax_type: Mapped[str | None] = mapped_column(Text)
    rate: Mapped[float | None] = mapped_column(Float)
