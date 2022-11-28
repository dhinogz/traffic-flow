import agentpy as ap
import numpy as np

from api.traffic_flow.services import normalization


class Car(ap.Agent):
    """ An agent with a position and velocity in a continuous space,
    who follows Craig Reynolds three rules of flocking behavior;
    plus a fourth rule to avoid the edges of the simulation space. """

    def setup(self):

        self.velocity =  [1.0, 0.000] 
        self.acceleration = [0 , 0]          
        self.close_car = False
        self.random = self.model.random
        self.group = self.random.choice(range(100))
        print(self.group)
        if self.group < self.p.problems:
            self.error = ((self.random.choice(range(self.p.problem_intensity))-self.p.problem_intensity/2)/self.p.problem_intensity)
        else:
            self.error = 0
        print(self.error)    

    def setup_pos(self, space):

        self.space = space
        self.neighbors = space.neighbors
        self.pos = space.positions[self]
        
    def update_velocity(self):

        pos = self.pos
        ndim = self.p.ndim

        nbs = self.neighbors(self, distance=self.p.outer_radius)
        nbs_len = 0
        nbs_pos_array = np.array(nbs.pos)
        v1 = np.zeros(ndim)
        for nbs_check in nbs_pos_array:
            if (nbs_check[0] -  pos[0]  > -1 and nbs_check[0] -  pos[0]  < self.p.outer_radius ) and (nbs_check[1] -  pos[1]  > -1 and nbs_check[1] -  pos[1]  < 1 ) :
                nbs_len += 1
        nbs_vec_array = np.array(nbs.velocity)
        if nbs_len > 0:
            if self.velocity[0] > 0.0:
                self.velocity =   [0, 0]   
            else:
                v1 = np.zeros(ndim)
        else:
            if self.velocity[0] < 1.0:
                v1 = np.array([1, 0.])
            else:
                v1 = np.zeros(ndim)

        
    
        self.velocity += v1
        self.velocity = normalization(self.velocity)+normalization(self.velocity)*self.error
        if pos[0] > 99:
            self.velocity = [1,0]

    def update_position(self):

        self.space.move_by(self, self.velocity)


    def remove_agent(self):
        """ Removes agents from the space. """
        
        #if self.pos[0] > 90:
    
class CarIncor(ap.Agent):
    """ An agent with a position and velocity in a continuous space,
    who follows Craig Reynolds three rules of flocking behavior;
    plus a fourth rule to avoid the edges of the simulation space. """

    def setup(self):

        self.velocity =  [1.0, 0.1] 
        self.acceleration = [0 , 0]          
        self.car_incor = False
        self.random = self.model.random
        self.group = self.random.choice(range(100))
        print(self.group)
        if self.group < self.p.problems:
            self.error = ((self.random.choice(range(self.p.problem_intensity))-self.p.problem_intensity/2)/self.p.problem_intensity)
        else:
            self.error = 0
        print(self.error)    

    def setup_pos(self, space):

        self.space = space
        self.neighbors = space.neighbors
        self.pos = space.positions[self]
        
    def update_velocity(self):

        pos = self.pos
        ndim = self.p.ndim

        

        nbs = self.neighbors(self, distance=self.p.outer_radius)
        nbs_len = 0
        nbs_pos_array = np.array(nbs.pos)
        for nbs_check in nbs_pos_array:
            if pos[1] >= 5.0:
                if (nbs_check[0] -  pos[0]  > 0 and nbs_check[0] -  pos[0]  < self.p.outer_radius ) and (nbs_check[1] -  pos[1]  > -1 and nbs_check[1] -  pos[1]  < 1 ) :
                    nbs_len += 1
            else:
                if (nbs_check[0] -  pos[0]  > 1 and nbs_check[0] -  pos[0]  < self.p.inner_radius*0.5 ) and (nbs_check[1] -  pos[1]  > -1 and nbs_check[1] -  pos[1]  < 1 ) :
                    nbs_len += 1

        #nbs_vec_array = np.array(nbs.velocity)
        v1 = np.zeros(ndim)
        if pos[1] >= 5.0:
            if not self.car_incor:
                self.velocity = [1, 0.] # Cambiar 10 por velocidad a la cual se tiene que disminuir
                self.car_incor = True
            if nbs_len > 0:
                if self.velocity[0] > 0.0:
                    self.velocity =  [0, 0]   
                else:
                    v1 = np.zeros(ndim)
            else:
                if self.velocity[0] < 1.0:
                    v1 = np.array([1.0, 0.])
                else:
                    v1 = np.zeros(ndim)
        else:
            if nbs_len > 0:
                if self.velocity[0] > 0.0:
                    self.velocity =   [0, 0]   
            else:
                if self.velocity[0] < 10.0:
                    self.velocity =   [1.0, 0.1]  


        self.velocity += v1
        self.velocity = normalization(self.velocity)+normalization(self.velocity)*self.error

        if pos[0] > 99:
            self.velocity = [1,0]
        
    def update_position(self):

        self.space.move_by(self, self.velocity)
        if self.pos[1]>=5.0:
            self.pos[1]=5.0
            #del self.space.positions[self]
        

class TrafficFlowModel(ap.Model):
    

    def setup(self):
        """ Initializes the agents and network of the model. """


        if self.p.cars_pos:
            # Initialize model with existing car positions
            self.space = ap.Space(self, shape=[self.p.size_x + self.p.outer_radius+5, self.p.size_y])
            self.agents = ap.AgentDList(self, self.p.population, Car)
            self.agentsIncor = ap.AgentDList(self, self.p.population_merge, CarIncor)
            self.space.add_agents(self.agents, self.p.cars_pos, random=False)
            self.space.add_agents(self.agentsIncor, self.p.cars_pos_merge, random=False)
            self.agents.setup_pos(self.space)
            self.agentsIncor.setup_pos(self.space)
            self.carrosNew = False
            self.carrosNewPop = 0
            self.carrosNewList = []


    def step(self):

        # Update velocity and position for cars in every step

        self.agents.update_velocity()  # Adjust direction
        self.agentsIncor.update_velocity() 
        self.agents.update_position()  # Move into new direction
        self.agentsIncor.update_position() 
        if self.carrosNew:
            for agentNew in self.carrosNewList:
                agentNew.update_velocity() 
                agentNew.update_position() 
        
        #self.remove_agent(self.agentsIncor)
        print(f"Iteracion t={self.t}")
        if self.t % 5 == 0 and self.t != 0:
            generacion = self.random.choice(range(100))
            if generacion < self.p.density:
                carrosEnInicio = 0
                for agent in self.agents:
                    if (agent.pos[0]  < self.p.outer_radius+1 ) :
                        carrosEnInicio += 1
                if self.carrosNew:
                    for carros in self.carrosNewList:
                        for agent in carros:
                            if (agent.pos[0]  < self.p.outer_radius+1 ) :
                                carrosEnInicio += 1
                if carrosEnInicio == 0 and self.carrosNew:
                    self.carrosNewList.append(ap.AgentDList(self, 1, Car))
                    self.space.add_agents(self.carrosNewList[len(self.carrosNewList)-1],[np.array([1, 5.])], random=False)
                    self.carrosNewList[len(self.carrosNewList)-1].setup_pos(self.space)
                elif carrosEnInicio == 0:
                    self.carrosNewList.append(ap.AgentDList(self, 1, Car))
                    self.space.add_agents(self.carrosNewList[0],[np.array([1, 5.])], random=False)
                    self.carrosNewList[0].setup_pos(self.space)
                    self.carrosNew = True

        
        if self.t % 5 == 0 and self.t != 0:
            generacion = self.random.choice(range(100))
            if generacion < self.p.density_merge:
                carrosEnInicio = 0
                for agent in self.agents:
                    if (agent.pos[0]  < self.p.outer_radius+21 and agent.pos[0]  > 18 ) and (agent.pos[1]  < 4 and agent.pos[1]  > 0 ) :
                        carrosEnInicio += 1
                if self.carrosNew:
                    for carros in self.carrosNewList:
                        for agent in carros:
                            if (agent.pos[0]  < self.p.outer_radius+21 and agent.pos[0]  > 18 ) and (agent.pos[1]  < 4 and agent.pos[1]  > 0 ) :
                                carrosEnInicio += 1
                if carrosEnInicio == 0 and self.carrosNew:
                    self.carrosNewList.append(ap.AgentDList(self, 1, CarIncor))
                    self.space.add_agents(self.carrosNewList[len(self.carrosNewList)-1],[np.array([20, 2.])], random=False)
                    self.carrosNewList[len(self.carrosNewList)-1].setup_pos(self.space)
                elif carrosEnInicio == 0:
                    self.carrosNewList.append(ap.AgentDList(self, 1, CarIncor))
                    self.space.add_agents(self.carrosNewList[0],[np.array([20, 2.])], random=False)
                    self.carrosNewList[0].setup_pos(self.space)
                    self.carrosNew = True
                    self.model.random

    


        # Check if any of the cars have a car nearby. If so, update agent.close_car to True

        # Update VSL value depending on density of cars in one specific area in grid.

    

    def calculate_VSL(self):
        # Calculate VSL inside a specific range
        pass