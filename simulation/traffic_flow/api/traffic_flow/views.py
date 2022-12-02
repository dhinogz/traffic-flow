from fastapi import APIRouter, Body

from .schemas import TrafficParams, CarRead
from .services import run_model

router = APIRouter()


@router.post("", response_model=list[CarRead])
async def get_traffic_model(traffic_params: TrafficParams = Body(...)) -> list[CarRead]:

    return run_model(traffic_params=traffic_params)
