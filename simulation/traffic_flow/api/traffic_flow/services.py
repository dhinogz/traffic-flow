import numpy as np
import pandas as pd

from .schemas import CarRead, PositionRead, TrafficParams

from models.traffic_flow import TrafficFlowModel


def run_model(traffic_params: TrafficParams) -> list[CarRead]:
    """
    Receive Pydantic model with parameters.
    Join those parameters and constant parameters needed for AgentPy.
    Run model and return parsed result.
    """

    constant_parameters = {
        "sizeX": 100,  # Constante que corresponde al tamaño en del borde x
        "sizeY": 10,  # Constante que corresponde al tamaño en del borde y
        "ndim": 2,  # Constante que corresponde a la dimension de la simulacion
        "population": 1,  # Constante que corresponde a la poblacion inicial de la autopista
        "populationIncor": 1,  # Constante que corresponde a la poblacion inicial de la incorporacion
        "cars_pos": [
            np.array([0, 5.0])
        ],  # Constante que corresponde a la posicion inicial de la autopista
        "cars_posIncor": [
            np.array([20, 2.0])
        ],  # Constante que corresponde a la posicion inicial de la incorporacion
    }

    parameters = {**traffic_params.dict(), **constant_parameters}

    model = TrafficFlowModel(parameters)

    results = model.run()

    return parse_model_results(results)


def parse_model_results(results: pd.DataFrame) -> list[CarRead]:
    """
    Receive result DataFrame from AgentPy.
    Results include two DataFrames (Car and CarIncor)

    Merge both result dataframes and sort by indexes id and t
    Use add_empty_step to add missing rows
    Traverse through all positions from every id and add rows to Pydantic model

    Return list of CarRead models.
    """

    df = pd.concat(
        [results["variables"]["Car"], results["variables"]["CarIncor"]]
    ).sort_values(by=["id", "t"])
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


def add_empty_steps(df) -> pd.core.groupby.GroupBy:
    """
    Add "empty" rows where position x and y are 0.
    Empty rows are defined by missing steps, starting at first step from every id and ending at 1.

    Return a GroupBy data type
    """

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
                df.loc[(car_id, current_step), :] = (current_step, car_id, 0, 0)
                current_step -= 1

    df = df.sort_values(by=["id", "time"])

    groups = df.groupby("id").agg(lambda x: list(x))

    return groups
