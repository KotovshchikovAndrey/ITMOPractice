import typing as tp

from fastapi import APIRouter, Depends
from kink import di

from domain.services.city_point_service import CityPointService
from infrastructure.config.settings import settings

router = APIRouter(prefix=f"{settings.api_prefix}")


@router.get("/test")
async def test_route(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
):
    await service.test_init()
    return "OK"
