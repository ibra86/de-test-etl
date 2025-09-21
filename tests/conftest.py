from typing import Any

import pytest

from etl.models import Order


@pytest.fixture
def minimal_order_dict() -> dict[str, Any]:
    return {
        "InternalOrderId": 1001,
        "OrderDateUtc": "2024-01-01T10:00:00",
        "LastUpdatedDateUtc": "2024-01-01T10:30:00",
        "BillingCustomer": {
            "InternalCustomerId": 5001,
            "UserId": "user-1",
            "EmailAddress": "a@example.com",
            "FirstName": "Ann",
            "LastName": "Lee",
        },
        "BillingAddress": {"City": "X"},
        "ShippingAddress": {"City": "Y"},
        "LineItems": [{
            "InternalLineItemId": 9001, "SKU": "SKU-0", "QuantityOrdered": 1,
            "Taxes": [{"InternalTaxRateId": 7001, "Amount": 2.5, "TaxType": "VAT", "Rate": 0.2}],
            "CustomFields": [{"Name": "Color", "Value": "Blue"}],
        }],
        "OrderPayments": [{
            "InternalOrderPaymentId": 8001, "Amount": 42.0,
            "CustomFields": [{"Name": "TxnRef", "Value": "TX-1"}],
            "Status": "Authorized",
        }],
        "ShippingRate": [{"InternalShippingRateId": 6001}],
        "ShippingTaxes": [{"InternalTaxRateId": 7101, "Amount": 0.0, "TaxType": "None", "Rate": 0.0}],
    }


@pytest.fixture
def minimal_order_model(minimal_order_dict):
    return Order.model_validate(minimal_order_dict)
