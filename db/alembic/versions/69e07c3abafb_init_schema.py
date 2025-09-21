"""init schema

Revision ID: 69e07c3abafb
Revises: 
Create Date: 2025-09-21 20:40:12.346721

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '69e07c3abafb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('orders',
                    sa.Column('order_id', sa.BigInteger(), nullable=False),
                    sa.Column('external_order_id', sa.Text(), nullable=True),
                    sa.Column('order_date_utc', sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.Column('last_updated_date_utc', sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.Column('deadline_date_utc', sa.TIMESTAMP(timezone=True), nullable=True),
                    sa.Column('order_status', sa.Text(), nullable=True),
                    sa.Column('invoice_status', sa.Text(), nullable=True),
                    sa.Column('shipment_status', sa.Text(), nullable=True),
                    sa.Column('shipping_total', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('sub_total', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('discount_total', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('order_total', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('currency_code', sa.String(length=8), nullable=True),
                    sa.Column('channel', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('order_id', name=op.f('pk_orders'))
                    )
    op.create_table('addresses',
                    sa.Column('order_id', sa.BigInteger(), nullable=False),
                    sa.Column('address_type', sa.String(length=16), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=True),
                    sa.Column('external_address_id', sa.Text(), nullable=True),
                    sa.Column('first_name', sa.Text(), nullable=True),
                    sa.Column('last_name', sa.Text(), nullable=True),
                    sa.Column('company_name', sa.Text(), nullable=True),
                    sa.Column('address_line1', sa.Text(), nullable=True),
                    sa.Column('address_line2', sa.Text(), nullable=True),
                    sa.Column('address_line3', sa.Text(), nullable=True),
                    sa.Column('city', sa.Text(), nullable=True),
                    sa.Column('state', sa.Text(), nullable=True),
                    sa.Column('zip_code', sa.Text(), nullable=True),
                    sa.Column('country_code', sa.String(length=2), nullable=True),
                    sa.Column('latitude', sa.Float(), nullable=True),
                    sa.Column('longitude', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'],
                                            name=op.f('fk_addresses_order_id_orders'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', 'address_type', name=op.f('pk_addresses'))
                    )
    op.create_table('customers',
                    sa.Column('order_id', sa.BigInteger(), nullable=False),
                    sa.Column('internal_customer_id', sa.BigInteger(), nullable=True),
                    sa.Column('user_id', sa.Text(), nullable=True),
                    sa.Column('first_name', sa.Text(), nullable=True),
                    sa.Column('last_name', sa.Text(), nullable=True),
                    sa.Column('email_address', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'],
                                            name=op.f('fk_customers_order_id_orders'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', name=op.f('pk_customers'))
                    )
    op.create_table('line_items',
                    sa.Column('order_id', sa.BigInteger(), nullable=False),
                    sa.Column('line_item_id', sa.BigInteger(), nullable=False),
                    sa.Column('sku', sa.Text(), nullable=True),
                    sa.Column('product_name', sa.Text(), nullable=True),
                    sa.Column('item_name', sa.Text(), nullable=True),
                    sa.Column('quantity_ordered', sa.Integer(), nullable=True),
                    sa.Column('quantity_invoiced', sa.Integer(), nullable=True),
                    sa.Column('quantity_shipped', sa.Integer(), nullable=True),
                    sa.Column('unit_price', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('unit_discount', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('sub_total', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('total_tax', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('total', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'],
                                            name=op.f('fk_line_items_order_id_orders'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', 'line_item_id', name=op.f('pk_line_items'))
                    )
    op.create_table('payments',
                    sa.Column('order_id', sa.BigInteger(), nullable=False),
                    sa.Column('order_payment_id', sa.BigInteger(), nullable=False),
                    sa.Column('payment_id', sa.BigInteger(), nullable=True),
                    sa.Column('payment_type', sa.Text(), nullable=True),
                    sa.Column('status', sa.Text(), nullable=True),
                    sa.Column('amount', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('amount_authorized', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('amount_captured', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('last_updated_by_staff_id', sa.BigInteger(), nullable=True),
                    sa.Column('last_updated_by_staff_name', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], name=op.f('fk_payments_order_id_orders'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', 'order_payment_id', name=op.f('pk_payments'))
                    )
    op.create_table('shipping_rates',
                    sa.Column('order_id', sa.BigInteger(), nullable=False),
                    sa.Column('internal_shipping_rate_id', sa.BigInteger(), nullable=False),
                    sa.Column('backend_name', sa.Text(), nullable=True),
                    sa.Column('rate_code', sa.Text(), nullable=True),
                    sa.Column('current_rate', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'],
                                            name=op.f('fk_shipping_rates_order_id_orders'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', 'internal_shipping_rate_id', name=op.f('pk_shipping_rates'))
                    )
    op.create_table('shipping_taxes',
                    sa.Column('order_id', sa.BigInteger(), nullable=False),
                    sa.Column('internal_tax_rate_id', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('tax_type', sa.Text(), nullable=True),
                    sa.Column('rate', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'],
                                            name=op.f('fk_shipping_taxes_order_id_orders'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', 'internal_tax_rate_id', name=op.f('pk_shipping_taxes'))
                    )
    op.create_table('line_item_custom_fields',
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('line_item_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('value', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['order_id', 'line_item_id'],
                                            ['line_items.order_id', 'line_items.line_item_id'],
                                            name=op.f('fk_line_item_custom_fields_order_id_line_items'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', 'line_item_id', 'name', name=op.f('pk_line_item_custom_fields'))
                    )
    op.create_table('line_item_taxes',
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('line_item_id', sa.Integer(), nullable=False),
                    sa.Column('internal_tax_rate_id', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Numeric(precision=18, scale=4), nullable=True),
                    sa.Column('tax_type', sa.Text(), nullable=True),
                    sa.Column('rate', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['order_id', 'line_item_id'],
                                            ['line_items.order_id', 'line_items.line_item_id'],
                                            name=op.f('fk_line_item_taxes_order_id_line_items'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', 'line_item_id', 'internal_tax_rate_id',
                                            name=op.f('pk_line_item_taxes'))
                    )
    op.create_table('payment_custom_fields',
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('order_payment_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('value', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['order_id', 'order_payment_id'],
                                            ['payments.order_id', 'payments.order_payment_id'],
                                            name=op.f('fk_payment_custom_fields_order_id_payments'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id', 'order_payment_id', 'name',
                                            name=op.f('pk_payment_custom_fields'))
                    )


def downgrade() -> None:
    op.drop_table('payment_custom_fields')
    op.drop_table('line_item_taxes')
    op.drop_table('line_item_custom_fields')
    op.drop_table('shipping_taxes')
    op.drop_table('shipping_rates')
    op.drop_table('payments')
    op.drop_table('line_items')
    op.drop_table('customers')
    op.drop_table('addresses')
    op.drop_table('orders')
