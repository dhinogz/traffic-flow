import numpy as np
import pandas as pd

from .schemas import CarRead, PositionRead, TrafficParams



def normalization(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def add_empty_steps(df):
        
    groups = df.groupby("id").agg(lambda x: list(x))

    min_steps = {}
    for i in range(len(groups)):
        car_id = groups.iloc[i].name
        first_step = groups.iloc[i]["time"][0]

        if first_step not in min_steps:
            min_steps[first_step] = [car_id]
        else:
            min_steps[first_step].append(car_id)


    for key, value in min_steps.items():
        for car_id in value:
            current_step = key - 1
            while current_step > 0:
                df.loc[(car_id, current_step),:] = (current_step, car_id, 0, 0)
                current_step -= 1

    df = df.sort_values(by=['id', "time"])

    groups = df.groupby("id").agg(lambda x: list(x))

    return groups



def parse_model_results(results) -> list[CarRead]:
    
    df = pd.concat([results["variables"]["Car"], results["variables"]["CarIncor"]]).sort_values(by=['id', "t"])
    groups = add_empty_steps(df)

    cars = []
    for i in range(len(groups)):
        
        car_id = groups.iloc[i].name
        steps = groups.iloc[i]["time"]
        pos_x = groups.iloc[i]["x"]
        pos_y = groups.iloc[i]["y"]

        positions = []
        for step, x, y in zip(steps, pos_x, pos_y):
            position = PositionRead(step=step, pos_x=x, pos_y=y)
            positions.append(position)
        
        car_read = CarRead(car_id=car_id, positions=positions)

        cars.append(car_read)

    return cars


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

    results = model.run()

    return parse_model_results(results)


def run_constant_model():

    from models.traffic_flow import TrafficFlowModel


    parameters = {
        'sizeX': 100, #Constante que corresponde al tamaño en del borde x
        'sizeY': 10, #Constante que corresponde al tamaño en del borde y
        'ndim': 2, #Constante que corresponde a la dimension de la simulacion
        'population': 1, #Constante que corresponde a la poblacion inicial de la autopista
        'populationIncor': 1, #Constante que corresponde a la poblacion inicial de la incorporacion
        'cars_pos':[np.array([0, 5.])], #Constante que corresponde a la posicion inicial de la autopista
        'cars_posIncor':[np.array([20, 2.])], #Constante que corresponde a la posicion inicial de la incorporacion

        'steps': 200, #Variable que corresponde a la cantidad de steps que se van a generar
        'outer_radiusX': 3, #Variable que corresponde al radio de detection 
        'problemas':20, #Variable que corresponde a la probabilidad de que un agente presente problemas 
        'intensidad_problemas':20, #Variable que corresponde a la intensidad del problema (20 = +-10) 
        'densidad':60, #Variable que corresponde a la probabilidad de que se genere un agente autopista en una frecuencia 
        'densidad_incor':30, #Variable que corresponde a la probabilidad de que se genere un agente incorporacion en una frecuencia
        'velocidad_diferencia':40, #Variable que corresponde a la diferencia de velocidad entre la autopista y la incorporacion (1-velocidad_diferencia)
        'frecuencia': 5 #Variable que corresponde a la frecuencia en la cual se va revisar la generacion de agentes y la velocidadFuzzy
    }

    model = TrafficFlowModel(parameters)

    results = model.run()

    return parse_model_results(results)
