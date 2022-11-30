from fastapi import APIRouter, Body

from .schemas import TrafficParams, CarRead
from .services import run_model

router = APIRouter()


@router.get(
    "info",
    response_model=list[CarRead],
)
async def get_traffic_info() -> list[CarRead]:

    return [
        {
            "id": 1,
            "positions": [
                {
                    "step": 1,
                    "pos_x": 2,
                    "pos_y": 2,
                },
                {
                    "step": 2,
                    "pos_x": 3,
                    "pos_y": 2,
                },
            ]
        },
        {
            "id": 2,
            "positions": [
                {
                    "step": 2,
                    "pos_x": 2,
                    "pos_y": 2,
                },
                {
                    "step": 3,
                    "pos_x": 3,
                    "pos_y": 2,
                },
            ]
        },
    ]

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


@router.post(
    "", 
    response_model=list[CarRead]
)
async def get_traffic_model(traffic_params: TrafficParams = Body(...)) -> list[CarRead]:


    # return run_traffic_model(traffic_params=traffic_params)

    return [
        {
            "id": 1,
            "positions": [
                {
                    "step": 1,
                    "pos_x": 2,
                    "pos_y": 2,
                },
                {
                    "step": 2,
                    "pos_x": 3,
                    "pos_y": 2,
                },
            ]
        },
        {
            "id": 2,
            "positions": [
                {
                    "step": 2,
                    "pos_x": 2,
                    "pos_y": 2,
                },
                {
                    "step": 3,
                    "pos_x": 3,
                    "pos_y": 2,
                },
            ]
        },
    ]

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
