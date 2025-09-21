import pandas as pd
import pytest
from pydantic import ValidationError

from etl.transformations import orders_to_dataframes, parse_to_dataframes

TABLES = [
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


def assert_df_has_rows(df: pd.DataFrame, expected_rows: int):
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == expected_rows


def test_orders_to_dataframes_minimal(minimal_order_model):
    dfs = orders_to_dataframes([minimal_order_model])

    for key in TABLES:
        assert key in dfs, f"missing table: {key}"
        assert isinstance(dfs[key], pd.DataFrame)

    assert_df_has_rows(dfs["orders"], 1)
    assert_df_has_rows(dfs["customers"], 1)
    assert_df_has_rows(dfs["addresses"], 2)
    assert_df_has_rows(dfs["line_items"], 1)
    assert_df_has_rows(dfs["line_item_taxes"], 1)
    assert_df_has_rows(dfs["line_item_custom_fields"], 1)
    assert_df_has_rows(dfs["payments"], 1)
    assert_df_has_rows(dfs["payment_custom_fields"], 1)
    assert_df_has_rows(dfs["shipping_rates"], 1)
    assert_df_has_rows(dfs["shipping_taxes"], 1)

    order_id = dfs["orders"].iloc[0]["order_id"]
    assert order_id is not None
    assert set(dfs["addresses"]["address_type"]) == {"billing", "shipping"}
    assert set(dfs["payments"]["status"]) == {"Authorized"}

    # every child order_id exists in orders
    orders_ids = set(dfs["orders"]["order_id"])
    for child in ["addresses", "line_items", "payments", "shipping_rates", "shipping_taxes"]:
        assert set(dfs[child]["order_id"]).issubset(orders_ids), f"FK mismatch in {child}"


def test_parse_to_dataframes_accepts_list_of_dicts(minimal_order_dict):
    dfs = parse_to_dataframes([minimal_order_dict])
    assert isinstance(dfs, dict)
    assert "orders" in dfs and dfs["orders"].shape[0] == 1
    assert "line_items" in dfs and dfs["line_items"].shape[0] == 1


def test_multiple_nested_items():
    o1 = {
        "InternalOrderId": 1002,
        "ExternalOrderId": "EXT-1002",
        "OrderDateUtc": "2024-01-03T12:00:00",
        "LastUpdatedDateUtc": "2024-01-03T13:00:00",
        "LineItems": [
            {
                "InternalLineItemId": 9101,
                "SKU": "SKU-1",
                "QuantityOrdered": 2,
                "Taxes": [{"InternalTaxRateId": 7201, "Amount": 1.0, "TaxType": "VAT", "Rate": 0.2}],
                "CustomFields": [{"Name": "Size", "Value": "M"}],
            },
            {"InternalLineItemId": 9102, "SKU": "SKU-2", "QuantityOrdered": 1, "Taxes": [], "CustomFields": []},
        ],
        "OrderPayments": [
            {"InternalOrderPaymentId": 8101, "Amount": 50.0, "CustomFields": [{"Name": "TxnRef", "Value": "TX-2"}]}
        ],
        "ShippingRate": [{"InternalShippingRateId": 6101}],
        "ShippingTaxes": [{"InternalTaxRateId": 7301, "Amount": 0.0, "TaxType": "None", "Rate": 0.0}],
    }
    o2 = {
        "InternalOrderId": 1003,
        "OrderDateUtc": "2024-01-04T10:00:00",
        "LastUpdatedDateUtc": "2024-01-04T10:30:00",
        "LineItems": [{"InternalLineItemId": 9201, "QuantityOrdered": 3, "Taxes": [], "CustomFields": []}],
        "OrderPayments": [],
        "ShippingRate": [],
        "ShippingTaxes": [],
    }

    dfs = parse_to_dataframes([o1, o2])

    assert len(dfs["orders"]) == 2
    assert len(dfs["line_items"]) == 3
    assert len(dfs["line_item_taxes"]) == 1
    assert len(dfs["payment_custom_fields"]) == 1
    assert len(dfs["shipping_rates"]) == 1
    assert len(dfs["shipping_taxes"]) == 1


def test_empty_input_returns_empty_frames():
    dfs = parse_to_dataframes([])
    for k in TABLES:
        assert k in dfs
        assert dfs[k].empty


def test_bad_input_raises_validation_error():
    with pytest.raises(ValidationError):
        parse_to_dataframes([{"InternalOrderId": "not-an-int"}])


def test_schema_columns_stable(minimal_order_dict):
    dfs = parse_to_dataframes([minimal_order_dict])
    expected_order_cols = {
        "order_id", "external_order_id", "order_date_utc", "last_updated_date_utc"
    }
    assert expected_order_cols.issubset(set(dfs["orders"].columns))
