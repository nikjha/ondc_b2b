from typing import List, Dict
from pydantic import BaseModel


class Descriptor(BaseModel):
    name: str
    code: str = ""


class Price(BaseModel):
    value: str
    currency: str


class Address(BaseModel):
    ward: str
    country: str
    building: str
    state: str
    city: str
    locality: str
    door: str
    area_code: str
    street: str


class Item(BaseModel):
    id: str
    descriptor: Descriptor
    tags: Dict[str, str]
    fulfillment_id: str
    payment_id: str


class Provider(BaseModel):
    id: str
    descriptor: Descriptor


class Breakup(BaseModel):
    title: str
    price: Price


class Quote(BaseModel):
    value: str
    currency: str
    breakup: List[Breakup]


class StateDescriptor(BaseModel):
    descriptor: Descriptor


class FulfillmentStartAuthorization(BaseModel):
    type: str
    token: str


class FulfillmentStartLocation(BaseModel):
    authorization: FulfillmentStartAuthorization


class Location(BaseModel):
    gps: str
    address: Address


class FulfillmentEndLocation(BaseModel):
    location: Location


class Agent(BaseModel):
    name: str
    phone: str
    rateable: bool
    rating: str


class Vehicle(BaseModel):
    category: str
    registration: str


class Person(BaseModel):
    name: str
    phone: str
    tags: Dict[str, str]


class Customer(BaseModel):
    person: Person


class Fulfillment(BaseModel):
    id: str
    state: StateDescriptor
    start: FulfillmentStartLocation
    end: FulfillmentEndLocation
    agent: Agent
    vehicle: Vehicle
    customer: Customer


class Payment(BaseModel):
    id: str
    type: str
    params: Dict[str, str]


class Order(BaseModel):
    id: str
    provider: Provider
    items: List[Item]
    quote: Quote
    fulfillment: Fulfillment
    payment: Payment


class OnConfirmMessage(BaseModel):
    order: Order


class OnConfirmContext(BaseModel):
    country: str
    bpp_uri: str
    domain: str
    timestamp: str
    bap_id: str
    bpp_id: str
    transaction_id: str
    message_id: str
    city: str
    core_version: str
    action: str
    bap_uri: str


class OnConfirmBody(BaseModel):
    context: OnConfirmContext
    message: OnConfirmMessage


class OnConfirm(BaseModel):
    post: OnConfirmBody
