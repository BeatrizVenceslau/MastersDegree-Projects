from aasma import Agent

# N_ACTIONS = 2
# GAS, BREAK = range(N_ACTIONS)

class CautiousAgent(Agent):

    """
    A baseline agent for the SimplifiedPredatorPrey environment.
    The greedy agent finds the nearest prey and moves towards it.
    """

    def __init__(self, agent_id, n_agents):
        super(CautiousAgent, self).__init__(f"Cautious Agent", n_agents, agent_id)
        self.next_action = 1

    def action(self, intentions) -> int:
        return self.next_action

    def intention(self, intentions) -> int:
        self.update_information()

        self.next_action = 1
        dependency = -1

        if self.front_square:
            obs = self.split_observations()
            f_id, _, _ = self.split_square_observation(obs[self.front_square])
            self.next_action = 0 if f_id == 0 else 1
            dependency = -1 if f_id == 0 else f_id

        next_coords = self.calculate_next_coords(self.next_action)

        intentions[self.agent_id] = (self.coords, next_coords, self.turn_dir, dependency)