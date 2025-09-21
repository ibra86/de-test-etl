import os

import pandas as pd
from sqlalchemy import create_engine, MetaData, text

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

engine = create_engine(os.getenv("DATABASE_URL", ""))

TABLE_ORDER = [
    "orders",
    "customers",
    "addresses",
    "line_items",
    "line_item_taxes",
    "line_item_custom_fields",
    "payments",
    "payment_custom_fields",
    "shipping_rates",
    "shipping_taxes",
]

UPSERT_KEYS = {
    "orders": ["order_id"],
    "customers": ["order_id"],
    "addresses": ["order_id", "address_type"],
    "line_items": ["order_id", "line_item_id"],
    "line_item_taxes": ["order_id", "line_item_id", "internal_tax_rate_id"],
    "line_item_custom_fields": ["order_id", "line_item_id", "name"],
    "payments": ["order_id", "order_payment_id"],
    "payment_custom_fields": ["order_id", "order_payment_id", "name"],
    "shipping_rates": ["order_id", "internal_shipping_rate_id"],
    "shipping_taxes": ["order_id", "internal_tax_rate_id"],
}


def load(dfs: dict[str, pd.DataFrame]) -> None:
    md = MetaData()
    md.reflect(bind=engine)

    with engine.begin() as conn:
        for name in TABLE_ORDER:
            df = dfs.get(name)
            if df is None or df.empty:
                continue

            for col in ("order_date_utc", "last_updated_date_utc", "deadline_date_utc"):
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], utc=True)

            # upsert logic:
            table = md.tables[name]
            keys = UPSERT_KEYS[name]

            # 1) key columns
            key_col_defs = ", ".join(
                f'{k} {table.c[k].type.compile(dialect=conn.dialect)}'
                for k in keys
            )
            tmp = f"tmp_keys_{name}"
            conn.execute(text(f'CREATE TEMP TABLE {tmp} ({key_col_defs}) ON COMMIT DROP'))

            # 2) load key values into tmp
            df_keys = df.loc[:, keys].copy()
            df_keys.to_sql(tmp, conn, if_exists="append", index=False, method="multi", chunksize=1000)

            # 3) del rows with tmp keys
            on_clause = " AND ".join([f"{name}.{k} = {tmp}.{k}" for k in keys])
            conn.execute(text(f"DELETE FROM {name} USING {tmp} WHERE {on_clause}"))

            # 4) append
            df.to_sql(name, conn, if_exists="append", index=False, method="multi", chunksize=1000)

            print(f"{name}: deleted duplicates and inserted {len(df)} rows")
