from typing import Dict, List, Optional
from pydantic import BaseModel


class Agent(BaseModel):
    name: str
    rateable: bool
    rating: str


class Person(BaseModel):
    name: str
    phone: str
    tags: Dict[str, str]


class Address(BaseModel):
    area_code: str
    building: str
    city: str
    country: str
    door: Optional[str] = None
    locality: str
    state: str
    street: str
    ward: str


class Location(BaseModel):
    address: Address
    gps: str


class Vehicle(BaseModel):
    category: str


class FulfillmentEndConfirm(BaseModel):
    location: Location


class FulfillmentStart(BaseModel):
    location: Location


class Customer(BaseModel):
    person: Person


class Fulfillment(BaseModel):
    agent: Agent
    customer: Customer
    end: FulfillmentEndConfirm
    id: str
    start: FulfillmentStart
    vehicle: Vehicle


class ItemDescriptor(BaseModel):
    code: str
    name: str


class ItemTagGroup(BaseModel):
    descriptor: ItemDescriptor
    list: List[Dict[str, str]]


class Item(BaseModel):
    descriptor: ItemDescriptor
    fulfillment_id: str
    id: str
    payment_id: str
    tags: Dict[str, str]


class PaymentParams(BaseModel):
    amount: str
    currency: str
    transaction_status: str


class Payment(BaseModel):
    id: str
    params: PaymentParams
    type: str


class ProviderDescriptor(BaseModel):
    name: str


class Provider(BaseModel):
    descriptor: ProviderDescriptor
    id: str


class Price(BaseModel):
    value: str
    currency: str


class QuoteBreakup(BaseModel):
    price: Price
    title: str


class Quote(BaseModel):
    breakup: List[QuoteBreakup]
    currency: str
    value: str


class Order(BaseModel):
    id : str
    fulfillment: Fulfillment
    items: List[Item]
    payment: Payment
    provider: Provider
    quote: Quote


class ConfirmMessage(BaseModel):
    order: Order
