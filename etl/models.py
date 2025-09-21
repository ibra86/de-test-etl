from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Address(BaseModel):
    id: Optional[int] = Field(None, alias="Id")
    external_address_id: Optional[str] = Field(None, alias="ExternalAddressId")
    first_name: Optional[str] = Field(None, alias="FirstName")
    last_name: Optional[str] = Field(None, alias="LastName")
    company_name: Optional[str] = Field(None, alias="CompanyName")
    address_line1: Optional[str] = Field(None, alias="AddressLine1")
    address_line2: Optional[str] = Field(None, alias="AddressLine2")
    address_line3: Optional[str] = Field(None, alias="AddressLine3")
    city: Optional[str] = Field(None, alias="City")
    state: Optional[str] = Field(None, alias="State")
    zip_code: Optional[str] = Field(None, alias="ZipCode")
    country_code: Optional[str] = Field(None, alias="CountryCode")
    latitude: Optional[float] = Field(None, alias="Latitude")
    longitude: Optional[float] = Field(None, alias="Longitude")


class Customer(BaseModel):
    first_name: Optional[str] = Field(None, alias="FirstName")
    last_name: Optional[str] = Field(None, alias="LastName")
    email_address: Optional[str] = Field(None, alias="EmailAddress")
    internal_customer_id: Optional[int] = Field(None, alias="InternalCustomerId")
    external_customer_id: Optional[str] = Field(None, alias="ExternalCustomerId")
    user_id: Optional[str] = Field(None, alias="UserId")


class Tax(BaseModel):
    internal_tax_rate_id: Optional[int] = Field(None, alias="InternalTaxRateId")
    amount: Optional[float] = Field(None, alias="Amount")
    backend_name: Optional[str] = Field(None, alias="BackendName")
    public_tax_name: Optional[str] = Field(None, alias="PublicTaxName")
    tax_type: Optional[str] = Field(None, alias="TaxType")
    rate: Optional[float] = Field(None, alias="Rate")


class CustomField(BaseModel):
    name: str = Field(alias="Name")
    value: Optional[object] = Field(None, alias="Value")


class LineItem(BaseModel):
    internal_line_item_id: int = Field(alias="InternalLineItemId")
    product_name: Optional[str] = Field(None, alias="ProductName")
    item_name: Optional[str] = Field(None, alias="ItemName")
    description: Optional[str] = Field(None, alias="Description")
    quantity_invoiced: Optional[int] = Field(None, alias="QuantityInvoiced")
    quantity_shipped: Optional[int] = Field(None, alias="QuantityShipped")
    quantity_cancelled: Optional[int] = Field(None, alias="QuantityCancelled")
    quantity_returned: Optional[int] = Field(None, alias="QuantityReturned")
    sub_total: Optional[float] = Field(None, alias="SubTotal")
    total_tax: Optional[float] = Field(None, alias="TotalTax")
    total: Optional[float] = Field(None, alias="Total")
    is_pre_order: Optional[bool] = Field(None, alias="IsPreOrder")
    sku: Optional[str] = Field(None, alias="SKU")
    external_line_item_id: Optional[str] = Field(None, alias="ExternalLineItemId")
    quantity_ordered: Optional[int] = Field(None, alias="QuantityOrdered")
    unit_price: Optional[float] = Field(None, alias="UnitPrice")
    unit_discount: Optional[float] = Field(None, alias="UnitDiscount")
    taxes: List[Tax] = Field(default_factory=list, alias="Taxes")
    custom_fields: List[CustomField] = Field(default_factory=list, alias="CustomFields")


class LastUpdatedBy(BaseModel):
    staff_name: Optional[str] = Field(None, alias="StaffName")
    staff_id: Optional[int] = Field(None, alias="StaffId")


class OrderPayment(BaseModel):
    internal_order_payment_id: int = Field(alias="InternalOrderPaymentId")
    external_order_payment_id: Optional[str] = Field(None, alias="ExternalOrderPaymentId")
    payment_type: Optional[str] = Field(None, alias="PaymentType")
    payment_type_description: Optional[str] = Field(None, alias="PaymentTypeDescription")
    payment_id: Optional[int] = Field(None, alias="PaymentId")
    amount: Optional[float] = Field(None, alias="Amount")
    amount_authorized: Optional[float] = Field(None, alias="AmountAuthorized")
    amount_captured: Optional[float] = Field(None, alias="AmountCaptured")
    status: Optional[str] = Field(None, alias="Status")
    last_updated_by: Optional[LastUpdatedBy] = Field(None, alias="LastUpdatedBy")
    custom_fields: List[CustomField] = Field(default_factory=list, alias="CustomFields")


class ShippingRate(BaseModel):
    internal_shipping_rate_id: Optional[int] = Field(None, alias="InternalShippingRateId")
    public_shipping_rate_name: Optional[str] = Field(None, alias="PublicShippingRateName")
    backend_name: Optional[str] = Field(None, alias="BackendName")
    rate_code: Optional[str] = Field(None, alias="RateCode")
    current_rate: Optional[float] = Field(None, alias="CurrentRate")
    enable_return_label_generation: Optional[bool] = Field(None, alias="EnableReturnLabelGeneration")


class AdditionalInformation(BaseModel):
    c_transaction_code: Optional[str] = Field(None, alias="C_transactionCode")
    order_currency: Optional[str] = Field(None, alias="OrderCurrency")
    overriding_culture_name: Optional[str] = Field(None, alias="OverridingCultureName")
    ui_culture_name: Optional[str] = Field(None, alias="UICultureName")
    is_imported_order: Optional[bool] = Field(None, alias="IsImportedOrder")
    has_passed_preauth_fraud: Optional[bool] = Field(None, alias="HAS_PASSED_PREAUTH_FRAUD")
    startorder_server: Optional[str] = Field(None, alias="StartOrder_Server")
    has_orr_failure: Optional[bool] = Field(None, alias="HAS_ORR_FAILURE")


class Order(BaseModel):
    internal_order_id: int = Field(alias="InternalOrderId")
    external_order_id: Optional[str] = Field(None, alias="ExternalOrderId")
    order_date_utc: datetime = Field(alias="OrderDateUtc")
    last_updated_date_utc: datetime = Field(alias="LastUpdatedDateUtc")
    deadline_date_utc: Optional[datetime] = Field(None, alias="DeadlineDateUtc")
    order_status: Optional[str] = Field(None, alias="OrderStatus")
    invoice_status: Optional[str] = Field(None, alias="InvoiceStatus")
    shipment_status: Optional[str] = Field(None, alias="ShipmentStatus")
    ship_to_store: Optional[str] = Field(None, alias="ShipToStore")

    billing_customer: Optional[Customer] = Field(None, alias="BillingCustomer")
    billing_address: Optional[Address] = Field(None, alias="BillingAddress")
    shipping_address: Optional[Address] = Field(None, alias="ShippingAddress")

    line_items: List[LineItem] = Field(default_factory=list, alias="LineItems")
    order_payments: List[OrderPayment] = Field(default_factory=list, alias="OrderPayments")

    taxes: List[Tax] = Field(default_factory=list, alias="Taxes")
    shipping_rate: List[ShippingRate] = Field(default_factory=list, alias="ShippingRate")
    shipping_taxes: List[Tax] = Field(default_factory=list, alias="ShippingTaxes")

    shipping_total: Optional[float] = Field(None, alias="ShippingTotal")
    sub_total: Optional[float] = Field(None, alias="SubTotal")
    discount_total: Optional[float] = Field(None, alias="DiscountTotal")
    order_total: Optional[float] = Field(None, alias="OrderTotal")
    currency_code: Optional[str] = Field(None, alias="CurrencyCode")

    ui_culture_name: Optional[str] = Field(None, alias="UICultureName")
    estore_culture_name: Optional[str] = Field(None, alias="EStoreCultureName")
    channel: Optional[str] = Field(None, alias="Channel")
    additional_flags: Optional[str] = Field(None, alias="AdditionalFlags")
    comments: Optional[str] = Field(None, alias="Comments")
    origin_ip_address: Optional[str] = Field(None, alias="OriginIPAddress")

    custom_fields: List[CustomField] = Field(default_factory=list, alias="CustomFields")
    additional_information: Optional[AdditionalInformation] = Field(None, alias="AdditionalInformation")

    model_config = dict(populate_by_name=True)
