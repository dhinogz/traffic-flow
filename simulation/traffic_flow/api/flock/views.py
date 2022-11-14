from fastapi import APIRouter, Body

from .schemas import FlockParams

from models.flocking import BoidsModel

router = APIRouter()

@router.post("")
async def get_flocking_model(flock_params: FlockParams = Body(...)):

    model = BoidsModel(flock_params.dict())
    results = model.run()

    # print(results.record)
    return results.arrange()
