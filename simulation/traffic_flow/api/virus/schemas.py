parameters = {
    "population": 1000,
    "infection_chance": 0.3,
    "recovery_chance": 0.1,
    "initial_infection_share": 0.1,
    "number_of_neighbors": 2,
    "network_randomness": 0.5,
}

from pydantic import BaseModel


class VirusParams(BaseModel):

    population: int
    infection_chance: float
    recovery_chance: float
    initial_infection_share: float
    number_of_neighbors: int
    network_randomness: float

    class Config:
        schema_extra = {
            "example": {
                "population": 1000,
                "infection_chance": 0.3,
                "recovery_chance": 0.1,
                "initial_infection_share": 0.1,
                "number_of_neighbors": 2,
                "network_randomness": 0.5,
            }
        }
