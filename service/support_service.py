import datetime

import requests
from starlette.background import BackgroundTasks

from b2b import search_model, mock_utils
from b2b.search_model import OnSupport

BPP_URI = "http://127.0.0.1:8000/bpp/mock/"
BPP_ID = "seller-mock"

def send_on_support(url: str, on_support: OnSupport):
    return requests.post(url + "/on_support", json=on_support.model_dump())


class SupportService:

    def support_service(body: search_model.Support, background_task: BackgroundTasks):
        static_on_support: OnSupport = mock_utils.get_support_results()
        print(static_on_support)
        static_on_support.context.transaction_id = body.context.transaction_id
        static_on_support.context.message_id = body.context.message_id
        static_on_support.context.timestamp = datetime.datetime.utcnow()
        background_task.add_task(send_on_support, body.context.bap_uri, static_on_support)
        json_response = {
            "domain": "ONDC:TRV10",
            "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
            "bap_id": f"{body.context.bap_id}",
            "transaction_id": f"{body.context.transaction_id}",
            "message_id": f"{body.context.message_id}",
            "city": "std:080",
            "core_version": "0.9.4",
            "action": "search",
            "bap_uri": f"{body.context.bap_uri}",
            "bpp_id": f"{BPP_ID}",
            "bpp_uri": f"{BPP_URI}",
        }
        return {"context": json_response, "message": {"ack": {"status": "ACK"}}}
