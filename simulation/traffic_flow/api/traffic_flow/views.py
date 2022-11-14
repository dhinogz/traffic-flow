from fastapi import APIRouter, Body

from .schemas import TrafficParams

from models.traffic_flow import TrafficFlow

router = APIRouter()

@router.post("")
async def get_traffic_model(traffic_params: TrafficParams = Body(...)):

    model = TrafficFlow(traffic_params.dict())
    results = model.run()

    # print(results.record)
    return results.arrange()
