from fastapi import APIRouter
from starlette.background import BackgroundTasks

from b2b import search_model
from b2b.search_model import Confirm, Status, Support
from service import search_select_init_service, confirm_service, status_service, support_service

BPP_URI = "http://127.0.0.1:8000/bpp/mock/"
BPP_ID = "seller-mock"

router = APIRouter(
    prefix="/b2b/bpp/mock",
    tags=["B2b Seller"],
    responses={404: {"description": "This endpoint is not yet mocked."}},
)


@router.post("/search")
def get_catalogue(body: search_model.Search, background_task: BackgroundTasks):
    return search_select_init_service.SearchService.search_service(body, background_task)


@router.post("/select")
def get_select(body: search_model.Select, background_task: BackgroundTasks):
    return search_select_init_service.SelectService.select_service(body, background_task)


@router.post("/init")
def get_select(body: search_model.Init, background_task: BackgroundTasks):
    return search_select_init_service.InitService.init_service(body, background_task)


@router.post("/confirm")
def get_confirm(body: Confirm, background_task: BackgroundTasks):
    return confirm_service.ConfirmService.confirm_service(body, background_task)


@router.post("/status")
def get_status(body: Status, background_task: BackgroundTasks):
    return status_service.StatusService.status_service(body, background_task)


@router.post("/support")
def get_support(body: Support, background_task: BackgroundTasks):
    return support_service.SupportService.support_service(body, background_task)
