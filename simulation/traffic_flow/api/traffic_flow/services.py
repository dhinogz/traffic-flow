import numpy as np

from .schemas import StepRead, TrafficParams



def normalization(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def parse_model_results(results) -> list[StepRead]:
    pass


def run_model(traffic_params: TrafficParams) -> list[StepRead]:
    from models.traffic_flow import TrafficFlowModel


    model = TrafficFlowModel(traffic_params)

    res = model.run()

    return parse_model_results(res)

    