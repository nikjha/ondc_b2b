from pydantic import BaseModel


class StatusMessage(BaseModel):
    order_id: str
