import agentpy as ap
import numpy as np


def normalization(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


class Car(ap.Agent):

    # Agente de la autopista

    def setup(self):

        # Velocidad inicial con movimiento a X positiva

        self.velocity = [1.0, 0.000]

        # Revision aleatoria para la generacion de error de velocidad

        self.random = self.model.random
        self.group = self.random.choice(range(100))
        if self.group < self.p.problemas:
            self.error = (
                self.random.choice(range(self.p.intensidad_problemas))
                - self.p.intensidad_problemas / 2
            ) / self.p.intensidad_problemas
        else:
            self.error = 0

        # Declaracion de que el agente no es de la incorporacion

        self.isIncor = False

        # Declaracion de que el agente aun no llega a su fin

        self.isFinished = False

    def setup_pos(self, space):

        # Iniciacion en las posiciones iniciales

        self.space = space
        self.neighbors = space.neighbors
        self.pos = space.positions[self]

    def update_velocity(self, velocidadFuzzy):

        # Metodo para la declaracion de velocidad

        # Simplificacion de variable de posicion

        pos = self.pos

        # Revision de si esta por salirse del mapa

        if pos[0] > 99:

            # Si si, continuar con velocidad constante

            self.velocity = [1, 0]
        else:

            # Si no, iniciar proceso de toma de decision de velocidad

            # Simplificacion de variable del parametro de numero de dimensiones

            ndim = self.p.ndim

            # Revision de agentes dentro del radio "outer_radiusX"

            nbs = self.neighbors(self, distance=self.p.outer_radiusX)

            # Inicializacion de variable para contar vecinos

            nbs_len = 0

            # Extraccion de todas las posiciones d elos vecinos

            nbs_pos_array = np.array(nbs.pos)

            # Declaracion de v1 como un vector de 0s de ndim dimensiones

            v1 = np.zeros(ndim)

            # Corrimiento de todos los agentes que son vecinos en su radio para revisar cuales estan enfrente

            for nbs_check in nbs_pos_array:
                if (
                    nbs_check[0] - pos[0] > -0.5
                    and nbs_check[0] - pos[0] < self.p.outer_radiusX
                ) and (nbs_check[1] - pos[1] > -1 and nbs_check[1] - pos[1] < 1):

                    # Si si estan, agregar 1 al contador de vecinos

                    nbs_len += 1

            if nbs_len > 0:
                if self.velocity[0] > 0.0:

                    # Si la cantidad de vecinos es mayor a 0 y se esta avanzando, detente

                    self.velocity = [0, 0]
            else:

                if self.velocity[0] < 1.0:

                    # Si la cantidad de vecinos es igual a 0 y no se esta avanzando, avanza

                    v1 = np.array([1, 0.0])

            # Se realiza la suma para ajustar el vector al tipo de dato necesario para la normalization

            self.velocity += v1
            if pos[0] < 30:

                # Si se encuentra dentro del area del VSL, ajustar por la variable "velocidadFuzzy"

                self.velocity = (
                    normalization(self.velocity)
                    + normalization(self.velocity) * self.error
                ) * velocidadFuzzy
            else:

                # Si no, continua normal, donde normal es la normalization de velocidades ajustada por el posible error

                self.velocity = (
                    normalization(self.velocity)
                    + normalization(self.velocity) * self.error
                )

    def update_position(self, t):

        # Se realiza el desplazamiento en base a la velocidad normalizada

        self.space.move_by(self, self.velocity)

        # Se guardan los valores de posicion nuevas, asi como el paso correspondiente

        self.x = self.pos[0]
        self.y = self.pos[1]
        self.time = t
        if self.x < 100 and self.id != 2 and self.id != 3:

            # Si no se ha desplazado a mas alla del area visible, guardar los datos de posicion actual

            self.record(["time", "id", "x", "y"])

        elif self.x >= 100 and (not self.isFinished) and self.id != 3 and self.id != 2:

            # Si ya se ha desplazado a mas alla del area visible, guardar los datos de posicion final

            self.x = 100
            self.y = self.pos[1]
            self.time = t

            self.record(["time", "id", "x", "y"])

            self.isFinished = True


class CarIncor(ap.Agent):

    # Agente en la incorporacion y luego autopista

    def setup(self):

        # Velocidad inicial con movimiento a X positiva y Y positiva menor

        self.velocity = [1.0, 0.1]

        # Revision aleatoria para la generacion de error de velocidad

        self.random = self.model.random
        self.group = self.random.choice(range(100))
        if self.group < self.p.problemas:
            self.error = (
                self.random.choice(range(self.p.intensidad_problemas))
                - self.p.intensidad_problemas / 2
            ) / self.p.intensidad_problemas
        else:
            self.error = 0

        # Declaracion de que el agente no es de la incorporacion

        self.isIncor = True

        # Declaracion de que el agente aun no llega a su fin

        self.isFinished = False

    def setup_pos(self, space):

        # Iniciacion en las posiciones iniciales

        self.space = space
        self.neighbors = space.neighbors
        self.pos = space.positions[self]

    def update_velocity(self, velocidadFuzzy):

        # Metodo para la declaracion de velocidad

        # Simplificacion de variable de posicion

        pos = self.pos

        # Revision de si esta por salirse del mapa

        if pos[0] > 99:

            # Si si, continuar con velocidad constante

            self.velocity = [1, 0]
        else:

            # Si no, iniciar proceso de toma de decision de velocidad

            # Simplificacion de variable del parametro de numero de dimensiones

            ndim = self.p.ndim

            # Revision de agentes dentro del radio "outer_radiusX"

            nbs = self.neighbors(self, distance=self.p.outer_radiusX)

            # Inicializacion de variable para contar vecinos

            nbs_len = 0

            # Corrimiento de todos los agentes que son vecinos en su radio para revisar cuales estan enfrente

            for nbs_pos_array in nbs:
                isIncor = nbs_pos_array.isIncor

                # Se almacena si el vecino es de la incorporacion o no

                nbs_check = np.array(nbs_pos_array.pos)
                if pos[1] >= 5.0:

                    # Si el vehiculo esta en la autopista entonces se realiza un mismo proceso de revision de vecinos

                    if (
                        nbs_check[0] - pos[0] > -1
                        and nbs_check[0] - pos[0] < self.p.outer_radiusX
                    ) and (nbs_check[1] - pos[1] > -1 and nbs_check[1] - pos[1] < 1):
                        nbs_len += 1
                else:
                    if isIncor:
                        # Si el vehiculo esta en la incorporacion entonces se realiza dos proceso con cajas de distintos tamanos, el mas chico siendo si son de la incorporacion

                        if (
                            nbs_check[0] - pos[0] > 0
                            and nbs_check[0] - pos[0] < self.p.outer_radiusX
                        ) and (
                            nbs_check[1] - pos[1] > -1 and nbs_check[1] - pos[1] < 1
                        ):
                            nbs_len += 1
                    else:
                        if (
                            nbs_check[0] - pos[0] > 0.5
                            and nbs_check[0] - pos[0] < self.p.outer_radiusX
                        ) and (
                            nbs_check[1] - pos[1] > -1 and nbs_check[1] - pos[1] < 1
                        ):
                            nbs_len += 1

            # Declaracion de v1 como un vector de 0s de ndim dimensiones

            v1 = np.zeros(ndim)

            if pos[1] >= 5.0:

                # Se revisa si el agente esta en la autopista

                if not self.isIncor:

                    # Si se acaba de incorporar a la autopista pero no se ha cambiado la identificacion
                    # Se ajusta la velocidad y se declara como parte de la autopista

                    self.velocity = [1, 0.0]
                    self.isIncor = False
                if nbs_len > 0:

                    # Si la cantidad de vecinos es mayor a 0 y se esta avanzando, detente

                    if self.velocity[0] > 0.0:
                        self.velocity = [0, 0]
                else:

                    # Si la cantidad de vecinos es igual a 0 y no se esta avanzando, avanza

                    if self.velocity[0] < 1.0:
                        v1 = np.array([1.0, 0.0])

                # Se realiza la suma para ajustar el vector al tipo de dato necesario para la normalization

                self.velocity += v1

                # Y se implementa la normalization de velocidades ajustada por el posible error para la velocidad

                self.velocity = (
                    normalization(self.velocity)
                    + normalization(self.velocity) * self.error
                )
            else:

                # Si todavia es parte de la incorporacion

                if nbs_len > 0:
                    if self.velocity[0] > 0.0:

                        # Si la cantidad de vecinos es mayor a 0 y se esta avanzando, detente

                        self.velocity = [0, 0]
                else:
                    if self.velocity[0] < 1.0:

                        # Si la cantidad de vecinos es igual a 0 y no se esta avanzando, avanza en diagonal

                        self.velocity = [1.0, 0.1]

                # Se realiza la suma para ajustar el vector al tipo de dato necesario para la normalization

                self.velocity += v1

                # Se normaliza la velocidad junto con el error y se ajusta en base a la diferencia que se pide con la autopista.

                self.velocity = (
                    normalization(self.velocity)
                    + normalization(self.velocity) * self.error
                ) * ((100 - self.p.velocidad_diferencia) / 100)

    def update_position(self, t):

        # Se realiza el desplazamiento en base a la velocidad normalizada

        self.space.move_by(self, self.velocity)

        # Si se reliza el ajuste y se sobrepasa la posicion, se incorpora a la autopista

        if self.pos[1] >= 5.0:
            self.pos[1] = 5.0

        # Se guardan los valores de posicion nuevas, asi como el paso correspondiente

        self.x = self.pos[0]
        self.y = self.pos[1]
        self.time = t

        if self.x < 100 and self.id != 3 and self.id != 2:

            # Si no se ha desplazado a mas alla del area visible, guardar los datos de posicion actual

            self.record(["time", "id", "x", "y"])

        elif self.x >= 100 and (not self.isFinished) and self.id != 3 and self.id != 2:

            # Si ya se ha desplazado a mas alla del area visible, guardar los datos de posicion final
            self.x = 100
            self.y = self.pos[1]
            self.time = t

            self.record(["time", "id", "x", "y"])

            self.isFinished = True


class TrafficFlowModel(ap.Model):

    # Clase para la construccion y mantenimiento del ambiente

    def setup(self):

        if self.p.cars_pos:

            # Se inicializa el espacio con las dimensiones adicionales para que se salgan los agentes una vez completados sus trayectos.

            self.space = ap.Space(
                self, shape=[self.p.sizeX + self.p.outer_radiusX + 5, self.p.sizeY]
            )

            # Se inicializa la lista de agentes de tanto autopista e incorporacion inciales.

            self.agents = ap.AgentDList(self, self.p.population, Car)
            self.agentsIncor = ap.AgentDList(self, self.p.populationIncor, CarIncor)

            # Se agregan los agentes a la lista de agentes de tanto autopista e incorporacion inciales.

            self.space.add_agents(self.agents, self.p.cars_pos, random=False)
            self.space.add_agents(self.agentsIncor, self.p.cars_posIncor, random=False)

            # Se inicializa las posiciones de la lista de agentes de tanto autopista e incorporacion inciales.

            self.agents.setup_pos(self.space)
            self.agentsIncor.setup_pos(self.space)

            # Se agrega la variable correspondiente indicando que aun no se han agregado carros nuevos.

            self.carrosNew = False

            # Se inicializa la lista de los agentes aleatorios que se van a agregar

            self.carrosNewList = []

            # Se inicializa la lista de los agentes aleatorios que se van a agregar

            self.velocidadFuzzy = 1

        else:
            pass

    def step(self):
        self.stop

        # Se actualiza la velocidad de los agentes de autopista y la incorporacion

        self.agents.update_velocity(self.velocidadFuzzy)
        self.agentsIncor.update_velocity(self.velocidadFuzzy)

        # Se actualiza la posicion de los agentes de autopista y la incorporacion

        self.agents.update_position(self.t)
        self.agentsIncor.update_position(self.t)

        # Se realiza un proceso en donde cada cierto numero de steps existe la posibilidad de agregar un nuevo agente a la autopista

        if self.t % self.p.frecuencia == 0 and self.t != 0:

            # Se genera un numero aleatorio entre 1 y 100

            generacion = self.random.choice(range(100))
            if generacion < self.p.densidad:

                # Si el numero esta dentro de la densidad se inicia un proceso de revisar si existe un agente en el area de generacion

                carrosEnInicio = 0

                # Se revisa si alguno de los agentes iniciales

                for agent in self.agents:
                    if agent.pos[0] < self.p.outer_radiusX + 1:
                        carrosEnInicio += 1

                # Se revisa si alguno de los agentes aleatrios si se generaron

                if self.carrosNew:
                    for carros in self.carrosNewList:
                        for agent in carros:
                            if agent.pos[0] < self.p.outer_radiusX + 1:
                                carrosEnInicio += 1

                # Si no hay vehiculos en el area de inicio y ya se inicializo la lista de agentes

                if carrosEnInicio == 0 and self.carrosNew:

                    # Se inicializa la lista de agentes.

                    self.carrosNewList.append(ap.AgentDList(self, 1, Car))

                    # Se agrega con la posicion de inicio.

                    self.space.add_agents(
                        self.carrosNewList[len(self.carrosNewList) - 1],
                        [np.array([0, 5.0])],
                        random=False,
                    )

                    # Se inicializa en el espacio.

                    self.carrosNewList[len(self.carrosNewList) - 1].setup_pos(
                        self.space
                    )
                elif carrosEnInicio == 0:

                    # Si no hay vehiculos en el area de inicio y no se inicializo la lista de agentes

                    # Se inicializa la lista de agentes.

                    self.carrosNewList.append(ap.AgentDList(self, 1, Car))

                    # Se agrega con la posicion de inicio.

                    self.space.add_agents(
                        self.carrosNewList[0], [np.array([0, 5.0])], random=False
                    )

                    # Se inicializa en el espacio.

                    self.carrosNewList[0].setup_pos(self.space)

                    # Se cambia a ya inicializado la lista de agentes

                    self.carrosNew = True

        # Se realiza un proceso en donde cada cierto numero de steps existe la posibilidad de agregar un nuevo agente a la incorporacion

        if self.t % self.p.frecuencia == 0 and self.t != 0:

            # Se genera un numero aleatorio entre 1 y 100

            generacion = self.random.choice(range(100))
            if generacion < self.p.densidad_incor:

                # Si el numero esta dentro de la densidad se inicia un proceso de revisar si existe un agente en el area de generacion

                carrosEnInicio = 0

                # Se revisa si alguno de los agentes iniciales

                for agent in self.agentsIncor:
                    if (
                        agent.pos[0] < self.p.outer_radiusX + 21 and agent.pos[0] > 18
                    ) and (agent.pos[1] < 3 and agent.pos[1] > 0):
                        carrosEnInicio += 1

                # Se revisa si alguno de los agentes aleatrios si se generaron

                if self.carrosNew:
                    for carros in self.carrosNewList:
                        for agent in carros:
                            if (
                                agent.pos[0] < self.p.outer_radiusX + 21
                                and agent.pos[0] > 18
                            ) and (agent.pos[1] < 3 and agent.pos[1] > 0):
                                carrosEnInicio += 1

                # Si no hay vehiculos en el area de inicio y ya se inicializo la lista de agentes

                if carrosEnInicio == 0 and self.carrosNew:

                    # Se inicializa la lista de agentes.

                    self.carrosNewList.append(ap.AgentDList(self, 1, CarIncor))

                    # Se agrega con la posicion de inicio.

                    self.space.add_agents(
                        self.carrosNewList[len(self.carrosNewList) - 1],
                        [np.array([20, 2.0])],
                        random=False,
                    )

                    # Se inicializa en el espacio.

                    self.carrosNewList[len(self.carrosNewList) - 1].setup_pos(
                        self.space
                    )
                elif carrosEnInicio == 0:

                    # Si no hay vehiculos en el area de inicio y no se inicializo la lista de agentes

                    # Se inicializa la lista de agentes.

                    self.carrosNewList.append(ap.AgentDList(self, 1, CarIncor))

                    # Se agrega con la posicion de inicio.

                    self.space.add_agents(
                        self.carrosNewList[0], [np.array([20, 2.0])], random=False
                    )

                    # Se inicializa en el espacio.

                    self.carrosNewList[0].setup_pos(self.space)

                    # Se cambia a ya inicializado la lista de agentes

                    self.carrosNew = True

        if self.carrosNew:

            # Se revisa si se ha inicializado la lista de agentes aleatorios

            # Si si, se itera a travez de toda la lista para actualizar la velocidad y posicion

            for agentNew in self.carrosNewList:
                agentNew.update_velocity(self.velocidadFuzzy)
                agentNew.update_position(self.t)

        # Finalmente se realiza un proceso en donde cada cierto numero de steps se actualiza la variable "velocidadFuzzy"

        if self.t % self.p.frecuencia == 0 and self.t != 0:
            carrosFuzzy = 0
            carrosFuzzyVelocidad = 0

            # Primero se itera en las 3 listas de agentes y se revisa si alguno esta dentro del area de cuello de botella.
            # Si cualquier agente esta dentro del area se suma uno a "carrosFuzzy" y se suma su velocidad a "carrosFuzzyVelocidad".

            for agent in self.agents:
                if (agent.pos[0] < 70 and agent.pos[0] > 30) and (agent.pos[1] == 5):
                    carrosFuzzy += 1
                    carrosFuzzyVelocidad += agent.velocity[0]
            for agent in self.agentsIncor:
                if (agent.pos[0] < 70 and agent.pos[0] > 30) and (agent.pos[1] == 5):
                    carrosFuzzy += 1
                    carrosFuzzyVelocidad += agent.velocity[0]
            if self.carrosNew:
                for carros in self.carrosNewList:
                    for agent in carros:
                        if (agent.pos[0] < 70 and agent.pos[0] > 30) and (
                            agent.pos[1] == 5
                        ):
                            carrosFuzzy += 1
                            carrosFuzzyVelocidad += agent.velocity[0]
            if carrosFuzzy == 0:

                # Si no existen vehiculos, la velocidad se queda igual.

                self.velocidadFuzzy = 1
            elif carrosFuzzy < 40 / (self.p.outer_radiusX * 3):

                # Si la cantidad de vehiculos detecta es menor a la distancia entre 3 veces el radio de detection, la velocidad se queda igual.

                self.velocidadFuzzy = 1
            else:
                if carrosFuzzyVelocidad / carrosFuzzy > 0.8:

                    # Si la velocidad promedio es mayor a 0.8, la velocidad se queda igual.

                    self.velocidadFuzzy = 1
                elif carrosFuzzyVelocidad / carrosFuzzy > 0.6:

                    # Si la velocidad promedio es menor a 0.8 pero mayor a 0.6, la velocidad se reduce a 0.8 su valor original.

                    self.velocidadFuzzy = 0.8
                elif carrosFuzzyVelocidad / carrosFuzzy > 0.4:

                    # Si la velocidad promedio es menor a 0.6 pero mayor a 0.4, la velocidad se reduce a 0.6 su valor original.

                    self.velocidadFuzzy = 0.6
                else:

                    # Si la velocidad promedio es menor a 0.4 , la velocidad se reduce a 0.4 su valor original.

                    self.velocidadFuzzy = 0.4
