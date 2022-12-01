from pydantic import BaseModel


class PositionRead(BaseModel):
    step: int
    pos_x: float
    pos_y: float


class CarRead(BaseModel):
    car_id: int
    positions: list[PositionRead]


class TrafficParams(BaseModel):

    steps: int
    outer_radiusX: int
    problemas: int
    intensidad_problemas: int
    densidad: int
    densidad_incor: int
    velocidad_diferencia: int
    frecuencia: int

    class Config:
        schema_extra = {
            "example": {
                "steps": 200,
                "outer_radiusX": 3,
                "problemas": 20,
                "intensidad_problemas": 20,
                "densidad": 60,
                "densidad_incor": 30,
                "velocidad_diferencia": 40,
                "frecuencia": 5,
            }
        }
