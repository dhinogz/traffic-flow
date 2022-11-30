
from pydantic import BaseModel

from typing import Optional

class CarRead(BaseModel):
    id: int
    pos_x: float
    pos_y: float

class StepRead(BaseModel):
    step: int
    cars: list[CarRead]


class CarPositionCreate(BaseModel):
    car_id: int 
    pos_x: float
    pos_y: float


class TrafficParams(BaseModel):

    size_x: Optional[int]
    size_y: Optional[int]
    seed: Optional[int]
    steps: Optional[int]
    ndim: Optional[int]
    population: Optional[int]
    population_merge: Optional[int]
    inner_radius: Optional[int]
    outer_radius: Optional[int]
    problems: Optional[int]
    problem_intensity: Optional[int]
    density: Optional[int]
    density_merge: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "size_x": 100,
                "size_y": 10,
                "seed": 150,
                "steps": 10,
                "ndim": 2,
                "population": 5,
                "population_merge": 2,
                "inner_radius": 2,
                "outer_radius": 4,
                "problems": 5,
                "problem_intensity": 20,
                "density": 50,
                "density_merge": 30,
                "cars_pos": [
                    {
                        "car_id": 1,
                        "pos_x": 0,
                        "pos_y": 5
                    },
                    {
                        "car_id": 2,
                        "pos_x": 6,
                        "pos_y": 5
                    },
                    {
                        "car_id": 3,
                        "pos_x": 12,
                        "pos_y": 5
                    },
                    {
                        "car_id": 4,
                        "pos_x": 24,
                        "pos_y": 5
                    }
                ],
                "cars_pos_merge": [
                    {
                        "car_id": 5,
                        "pos_x": 20,
                        "pos_y": 2
                    },
                    {
                        "car_id": 6,
                        "pos_x": 30,
                        "pos_y": 3
                    }
                ]
            }
        }

