from pydantic import BaseModel


class FlockParams(BaseModel):

    size: int
    seed: int
    steps: int
    ndim: int
    population: int
    inner_radius: int
    outer_radius: int
    border_distance: int
    cohesion_strength: float
    seperation_strength: float
    alignment_strength: float
    border_strength: float

    class Config:
        schema_extra = {
            "example": {
                "size": 50,
                "seed": 123,
                "steps": 200,
                "ndim": 2,
                "population": 200,
                "inner_radius": 3,
                "outer_radius": 10,
                "border_distance": 10,
                "cohesion_strength": 0.005,
                "seperation_strength": 0.1,
                "alignment_strength": 0.3,
                "border_strength": 0.5,
            }
        }
