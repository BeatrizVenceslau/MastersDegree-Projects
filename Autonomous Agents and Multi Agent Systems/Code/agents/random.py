import numpy as np
from aasma import Agent

class RandomAgent(Agent):

    def __init__(self, agent_id, n_agents):
        super(RandomAgent, self).__init__("Random Agent", n_agents, agent_id)
        self.actions = np.arange(2)
        self.next_action = 0

    def action(self, intentions) -> int:
        return self.next_action

    def intention(self, intentions) -> int:
        self.update_information()

        self.next_action = np.random.choice(self.actions)

        next_coords = self.calculate_next_coords(self.next_action)

        intentions[self.agent_id] = (self.coords, next_coords, self.turn_dir, -1)