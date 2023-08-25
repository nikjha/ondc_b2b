import datetime
from uuid import uuid4

import requests
from starlette.background import BackgroundTasks

from config.db import database
from b2b import mock_utils
from b2b.search_model import Confirm, OnConfirm
from schemas.order_model import Order

BPP_URI = "http://127.0.0.1:8000/bpp/mock/"
BPP_ID = "seller-mock"


def send_on_confirm(url: str, on_confirm: OnConfirm):
    return requests.post(url + "/on_confirm", json=on_confirm.model_dump())


class ConfirmService:

    def confirm_service(body: Confirm, background_task: BackgroundTasks):
        static_on_confirm: OnConfirm = mock_utils.get_confirm_results()
        print(static_on_confirm)
        order_id = body.message.order.id
        static_on_confirm.context.transaction_id = body.context.transaction_id
        static_on_confirm.context.message_id = body.context.message_id
        static_on_confirm.context.timestamp = datetime.datetime.utcnow()
        static_on_confirm.message.order.id = order_id
        background_task.add_task(send_on_confirm, body.context.bap_uri, static_on_confirm)
        get_and_save_order(static_on_confirm, static_on_confirm.context.transaction_id,
                           static_on_confirm.context.message_id, order_id, body.context.bap_uri, body.context.bap_id)
        json_response = {
            "domain": "ONDC:TRV10",
            "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
            "bap_id": f"{body.context.bap_id}",
            "transaction_id": f"{body.context.transaction_id}",
            "message_id": f"{body.context.message_id}",
            "bpp_id": f"{BPP_ID}",
            "bpp_uri": f"{BPP_URI}",
            "city": "std:080",
            "core_version": "0.9.4",
            "action": f"{body.context.action}",
            "bap_uri": f"{body.context.bap_uri}",
        }
        return {"context": json_response, "message": {"ack": {"status": "ACK"}}}


def get_and_save_order(message: OnConfirm, transaction_id: str, message_id: str, order_id: str, bap_uri: str,
                       bap_id: str):
    confirm_data = message.message
    # Now create an instance of Order
    order = Order(order_id=order_id, order=message, message_id=message_id, transaction_id=transaction_id,
                  bap_uri=bap_uri, bap_id=bap_id, count=1)
    order_data = order.dict()
    print(order_data)
    orders_collection = database["order"]
    insert_result = orders_collection.insert_one(order_data)
