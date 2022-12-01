import agentpy as ap


class MyAgent(ap.Agent):
    def setup(self):
        # Initialize an attribute with a parameter
        self.my_attribute = self.p.my_parameter

    def agent_method(self):
        # Define custom actions here
        pass


class MyModel(ap.Model):
    def setup(self):
        """Initiate a list of new agents."""
        self.agents = ap.AgentList(self, self.p.agents, MyAgent)

    def step(self):
        """Call a method for every agent."""
        self.agents.agent_method()

    def update(self):
        """Record a dynamic variable."""
        self.agents.record("my_attribute")

    def end(self):
        """Repord an evaluation measure."""
        self.report("my_measure", 1)


parameters = {"my_parameter": 42, "agents": 10, "steps": 10}

model = MyModel(parameters)
results = model.run()

info = results.info
