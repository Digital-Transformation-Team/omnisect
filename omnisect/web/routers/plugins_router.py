from dishka import FromDishka
from dishka.integrations.fastapi import DishkaSyncRoute
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.services.plugin_service import PluginService


router = APIRouter(
    prefix="/api/plugins/v1", tags=["Plugins"], route_class=DishkaSyncRoute
)


@router.get("/")
def list_plugins(service: FromDishka[PluginService]):
    dto = service.list_plugins()
    return JSONResponse(content=jsonable_encoder(dto), status_code=status.HTTP_200_OK)


@router.get("/{web_id}")
def get_plugin(web_id: str, service: FromDishka[PluginService]):
    dto = service.get_plugin(web_id=web_id)
    return JSONResponse(content=jsonable_encoder(dto), status_code=status.HTTP_200_OK)


@router.post("/{web_id}")
def invoke_plugin(web_id: str, service: FromDishka[PluginService]):
    service.invoke_plugin(web_id=web_id)
    return JSONResponse(content=jsonable_encoder({}), status_code=status.HTTP_200_OK)
