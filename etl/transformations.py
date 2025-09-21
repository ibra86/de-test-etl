import pandas as pd

from etl.models import Order

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass


def orders_to_dataframes(objs: list[Order]) -> dict[str, pd.DataFrame]:
    rows_orders = []
    rows_customers = []
    rows_addresses = []
    rows_items = []
    rows_item_taxes = []
    rows_item_cfs = []
    rows_payments = []
    rows_payment_cfs = []
    rows_shipping_rates = []
    rows_shipping_taxes = []

    for o in objs:
        oid = o.internal_order_id

        rows_orders.append({
            "order_id": oid,
            "external_order_id": o.external_order_id,
            "order_date_utc": o.order_date_utc,
            "last_updated_date_utc": o.last_updated_date_utc,
            "deadline_date_utc": o.deadline_date_utc,
            "order_status": o.order_status,
            "invoice_status": o.invoice_status,
            "shipment_status": o.shipment_status,
            "shipping_total": o.shipping_total,
            "sub_total": o.sub_total,
            "discount_total": o.discount_total,
            "order_total": o.order_total,
            "currency_code": o.currency_code,
            "channel": o.channel,
        })

        if o.billing_customer:
            bc = o.billing_customer
            rows_customers.append({
                "order_id": oid,
                "internal_customer_id": bc.internal_customer_id,
                "user_id": bc.user_id,
                "first_name": bc.first_name,
                "last_name": bc.last_name,
                "email_address": bc.email_address,
            })

        if o.billing_address:
            rows_addresses.append(
                {"order_id": oid, "address_type": "billing", **o.billing_address.model_dump(by_alias=False)})
        if o.shipping_address:
            rows_addresses.append(
                {"order_id": oid, "address_type": "shipping", **o.shipping_address.model_dump(by_alias=False)})

        for li in o.line_items:
            lid = li.internal_line_item_id
            rows_items.append({
                "order_id": oid,
                "line_item_id": lid,
                "sku": li.sku,
                "product_name": li.product_name,
                "item_name": li.item_name,
                "quantity_ordered": li.quantity_ordered,
                "quantity_invoiced": li.quantity_invoiced,
                "quantity_shipped": li.quantity_shipped,
                "unit_price": li.unit_price,
                "unit_discount": li.unit_discount,
                "sub_total": li.sub_total,
                "total_tax": li.total_tax,
                "total": li.total,
            })
            for t in li.taxes:
                rows_item_taxes.append({
                    "order_id": oid,
                    "line_item_id": lid,
                    "internal_tax_rate_id": t.internal_tax_rate_id,
                    "amount": t.amount,
                    "tax_type": t.tax_type,
                    "rate": t.rate,
                })
            for cf in li.custom_fields:
                rows_item_cfs.append({
                    "order_id": oid,
                    "line_item_id": lid,
                    "name": cf.name,
                    "value": cf.value,
                })

        for p in o.order_payments:
            rows_payments.append({
                "order_id": oid,
                "order_payment_id": p.internal_order_payment_id,
                "payment_id": p.payment_id,
                "payment_type": p.payment_type,
                "status": p.status,
                "amount": p.amount,
                "amount_authorized": p.amount_authorized,
                "amount_captured": p.amount_captured,
                "last_updated_by_staff_id": p.last_updated_by.staff_id if p.last_updated_by else None,
                "last_updated_by_staff_name": p.last_updated_by.staff_name if p.last_updated_by else None,
            })
            for cf in p.custom_fields:
                rows_payment_cfs.append({
                    "order_id": oid,
                    "order_payment_id": p.internal_order_payment_id,
                    "name": cf.name,
                    "value": cf.value,
                })

        for r in o.shipping_rate:
            rows_shipping_rates.append({
                "order_id": oid,
                "internal_shipping_rate_id": r.internal_shipping_rate_id,
                "backend_name": r.backend_name,
                "rate_code": r.rate_code,
                "current_rate": r.current_rate,
            })
        for st in o.shipping_taxes:
            rows_shipping_taxes.append({
                "order_id": oid,
                "internal_tax_rate_id": st.internal_tax_rate_id,
                "amount": st.amount,
                "tax_type": st.tax_type,
                "rate": st.rate,
            })

    dfs = {
        "orders": pd.DataFrame(rows_orders),
        "customers": pd.DataFrame(rows_customers),
        "addresses": pd.DataFrame(rows_addresses),
        "line_items": pd.DataFrame(rows_items),
        "line_item_taxes": pd.DataFrame(rows_item_taxes),
        "line_item_custom_fields": pd.DataFrame(rows_item_cfs),
        "payments": pd.DataFrame(rows_payments),
        "payment_custom_fields": pd.DataFrame(rows_payment_cfs),
        "shipping_rates": pd.DataFrame(rows_shipping_rates),
        "shipping_taxes": pd.DataFrame(rows_shipping_taxes),
    }
    return dfs


def parse_to_dataframes(raw_json: list[dict]) -> dict[str, pd.DataFrame]:
    orders: list[Order] = [Order.model_validate(o) for o in raw_json]

    dfs = orders_to_dataframes(orders)
    return dfs
