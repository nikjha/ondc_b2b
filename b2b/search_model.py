from typing import Any

from pydantic import BaseModel

from b2b.confirm_model_response import ConfirmMessage
from b2b.status_model import StatusMessage
from b2b.order_model_message import OnConfirmMessage
from ondc.context import Context


class Search(BaseModel):
    context: Context
    message: Any


class OnSearch(BaseModel):
    context: Context
    message: Any


class Select(BaseModel):
    context: Context
    message: Any


class OnSelect(BaseModel):
    context: Context
    message: Any


class OnInit(BaseModel):
    context: Context
    message: Any


class Init(BaseModel):
    context: Context
    message: Any


class Confirm(BaseModel):
    context: Context
    message: ConfirmMessage


class OnConfirm(BaseModel):
    context: Context
    message: OnConfirmMessage


class Status(BaseModel):
    context: Context
    message: StatusMessage


class OnStatus(BaseModel):
    context: Context
    message: OnConfirmMessage


class SupportMessage(BaseModel):
    ref_id: str


class Support(BaseModel):
    context: Context
    message: SupportMessage


class OnSupportMessage(BaseModel):
    phone : str
    email : str
    url : str


class OnSupport(BaseModel):
    context: Context
    message: OnSupportMessage
