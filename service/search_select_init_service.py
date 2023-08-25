import datetime

import requests
from starlette.background import BackgroundTasks

from b2b import search_model, mock_utils
from b2b.search_model import OnSearch, OnSelect, OnInit

BPP_URI = "http://127.0.0.1:8000/bpp/mock/"
BPP_ID = "seller-mock"
url_text = 'https://preprod.gateway.ondc.org'


def send_on_search(url: "str", on_search: OnSearch):
    return requests.post(url_text + "/on_search", json=on_search.model_dump())


def send_on_select(url: str, on_select: OnSelect):
    return requests.post(url_text + "/on_select", json=on_select.model_dump())


def send_on_init(url: str, on_init: OnInit):
    return requests.post(url_text + "/on_init", json=on_init.model_dump())


class SearchService:

    def search_service(body: search_model.Search, background_task: BackgroundTasks):
        import pdb; pdb.set_trace()
        static_on_search: OnSearch = mock_utils.get_search_results()
        print(static_on_search)
        static_on_search.context.transaction_id = body.context.transaction_id
        static_on_search.context.message_id = body.context.message_id
        static_on_search.context.timestamp = datetime.datetime.utcnow()
        background_task.add_task(send_on_search, body.context.bap_uri, static_on_search)
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


class SelectService:

    def select_service(body: search_model.Select, background_task: BackgroundTasks):
        static_on_select: OnSelect = mock_utils.get_select_results()
        print(static_on_select)
        static_on_select.context.transaction_id = body.context.transaction_id
        static_on_select.context.message_id = body.context.message_id
        static_on_select.context.timestamp = datetime.datetime.utcnow()
        background_task.add_task(send_on_select, body.context.bap_uri, static_on_select)
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


class InitService:


    def init_service(body: search_model.Init, background_task: BackgroundTasks):
        static_on_init: OnSelect = mock_utils.get_init_results()
        print(static_on_init)
        static_on_init.context.transaction_id = body.context.transaction_id
        static_on_init.context.message_id = body.context.message_id
        static_on_init.context.timestamp = datetime.datetime.utcnow()
        background_task.add_task(send_on_init, body.context.bap_uri, static_on_init)
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
