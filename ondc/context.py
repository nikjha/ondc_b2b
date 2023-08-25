from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

BPP_URI = "http://127.0.0.1:8000/bpp/mock/"
BPP_ID = "seller-mock"


class Action(str, Enum):
    SEARCH = 'search'
    ON_SEARCH = 'on_search'
    SELECT = 'select'
    ON_SELECT = 'on_select'
    INIT = 'init'
    ON_INIT = 'on_init'
    CONFIRM = 'confirm'
    ON_CONFIRM = 'on_confirm'
    STATUS = 'status'
    ON_STATUS = 'on_status'
    SUPPORT = 'support'
    ON_SUPPORT = 'on_support'


class Domain(str, Enum):
    ONDC_TRV10 = 'ONDC:TRV10'


def utc_timestamp():
    return datetime.utcnow().isoformat()[:-3] + 'Z'


class Context(BaseModel):
    domain: Domain
    action: Action
    message_id: str
    transaction_id: str
    timestamp: str = Field(default_factory=utc_timestamp, )
    bap_id: str
    bap_uri: str
    bpp_id: Optional[str] = Field(default=BPP_ID)
    bpp_uri: Optional[str] = Field(default=BPP_URI)

    @field_serializer('timestamp')
    def serialize_dt(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'






