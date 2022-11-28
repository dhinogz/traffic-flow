from fastapi import APIRouter, Body

from .schemas import TrafficParams, StepRead

from models.traffic_flow import TrafficFlowModel

router = APIRouter()

@router.post(
    "", 
    # response_model=list[StepRead]
)
async def get_traffic_model(traffic_params: TrafficParams = Body(...)):

    # model = TrafficFlowModel(traffic_params.dict())
    # results = model.run()

    # # print(results.record)
    # return results.arrange()

    return [
            {
                "step": 1,
                "cars": [    
                    {
                        "id": 1,
                        "pos_x": 2,
                        "pos_y": 2,
                    },
                    {
                        "id": 2,
                        "pos_x": 4,
                        "pos_y": 2,
                    },
                    {
                        "id": 3,
                        "pos_x": 5,
                        "pos_y": 2,
                    },
                ],
            },
            {
                "step": 2,
                "cars": [    
                    {
                        "id": 1,
                        "pos_x": 2,
                        "pos_y": 2,
                    },
                    {
                        "id": 2,
                        "pos_x": 5,
                        "pos_y": 2,
                    },
                    {
                        "id": 3,
                        "pos_x": 6,
                        "pos_y": 2,
                    },
                ]
            }
        ]
