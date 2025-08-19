from dataclasses import dataclass

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.services.plugin_service import PluginService

router = APIRouter(prefix="/api/plugins/v1", tags=["Plugins"], route_class=DishkaRoute)


@dataclass
class InvokePluginBody:
    text: str


@router.get("/")
async def list_plugins(service: FromDishka[PluginService]):
    dto = service.list_plugins()
    return JSONResponse(content=jsonable_encoder(dto), status_code=status.HTTP_200_OK)


@router.get("/{web_id}")
async def get_plugin(web_id: str, service: FromDishka[PluginService]):
    dto = service.get_plugin(web_id=web_id)
    return JSONResponse(content=jsonable_encoder(dto), status_code=status.HTTP_200_OK)


@router.post("/{web_id}")
async def invoke_plugin(web_id: str, text: str, service: FromDishka[PluginService]):
    data = service.invoke_plugin(web_id=web_id, text=text)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)
