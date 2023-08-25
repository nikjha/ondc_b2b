from pydantic import BaseModel, Field

from b2b.search_model import OnConfirm


class Order(BaseModel):
    _id: str
    order_id: str
    order: OnConfirm
    message_id: str = Field(alias="message_id")
    transaction_id: str
    bap_uri: str
    bap_id: str
    count: int
