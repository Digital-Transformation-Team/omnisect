import os

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.dto import plugin_dto
from src.services.plugin_service import PluginService

router = APIRouter(prefix="/api/plugins/v1", tags=["Plugins"], route_class=DishkaRoute)


@router.get("/")
async def list_plugins(service: FromDishka[PluginService]):
    dto = service.list_plugins()
    return JSONResponse(content=jsonable_encoder(dto), status_code=status.HTTP_200_OK)


@router.get("/{web_id}")
async def get_plugin(web_id: str, service: FromDishka[PluginService]):
    dto = service.get_plugin(web_id=web_id)
    return JSONResponse(content=jsonable_encoder(dto), status_code=status.HTTP_200_OK)


@router.post("/{web_id}")
async def invoke_plugin(
    web_id: str,
    service: FromDishka[PluginService],
    body: plugin_dto.InvokePlugin,
    request: Request,
):
    outp = service.invoke_plugin(web_id=web_id, inp=body)

    if isinstance(outp.file_path, str) and os.path.isfile(outp.file_path):
        file_name = os.path.basename(outp.file_path)
        file_url = str(request.base_url) + f"outputs/{file_name}"
        return JSONResponse(
            content=jsonable_encoder({"file_url": file_url}),
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content=jsonable_encoder(outp),
        status_code=status.HTTP_200_OK,
    )
