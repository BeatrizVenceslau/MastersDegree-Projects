from aasma import Agent

class GreedyAgent(Agent):

    def __init__(self, agent_id, n_agents):
        super(GreedyAgent, self).__init__("Greedy Agent", n_agents, agent_id)
        self.next_action = 0 #does not stop

    def action(self, intentions) -> int:
        return self.next_action

    def intention(self, intentions) -> int:
        self.update_information()

        next_coords = self.calculate_next_coords(self.next_action)

        intentions[self.agent_id] = (self.coords, next_coords, self.turn_dir, -1)