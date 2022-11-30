import numpy as np

from .schemas import CarRead, TrafficParams



def normalization(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def parse_model_results(results) -> list[CarRead]:
    pass


def run_model(traffic_params: TrafficParams) -> list[CarRead]:
    from models.traffic_flow import TrafficFlowModel

    constant_parameters = {
        'sizeX': 100, #Constante que corresponde al tamaño en del borde x
        'sizeY': 10, #Constante que corresponde al tamaño en del borde y
        'ndim': 2, #Constante que corresponde a la dimension de la simulacion
        'population': 1, #Constante que corresponde a la poblacion inicial de la autopista
        'populationIncor': 1, #Constante que corresponde a la poblacion inicial de la incorporacion
        'cars_pos':[np.array([0, 5.])], #Constante que corresponde a la posicion inicial de la autopista
        'cars_posIncor':[np.array([20, 2.])], #Constante que corresponde a la posicion inicial de la incorporacion
    }

    parameters = {**traffic_params.dict(), **constant_parameters}

    model = TrafficFlowModel(parameters)

    res = model.run()

    # pandas.concat([results["variables"]["Car"], results["variables"]["CarIncor"]]).sort_values(by=['id', "t"])

    return parse_model_results(res)

    