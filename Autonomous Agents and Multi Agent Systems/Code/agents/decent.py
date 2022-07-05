from aasma import Agent

class DecentAgent(Agent):

    junction_entrance = [8, 7], [5, 6], [6, 8], [7, 5]

    def __init__(self, agent_id, n_agents):
        super(DecentAgent, self).__init__(f"Decent Agent", n_agents, agent_id)
        self.next_action = 1
        self.diagonal_square = None

    def find_junction_problem(self, intentions):
        ids = []

        for k in intentions:
            data = intentions[k]
            if not data: continue

            coords, next_coords, dir, _ = intentions[k]
            if dir == 1: continue
            if coords == next_coords: continue
            if 5 not in coords and 8 not in coords: continue
            ids.append(k)
        
        if len(ids) >= 4:
            return max(ids)
        
        return -1


    def action(self, intentions) -> int:

        #If already turned always has priority
        if self.turned: return self.next_action

        # If 4 in junction, get the greatest id
        greatest_id_junction = self.find_junction_problem(intentions)

        # If problem found and I'm the "loser", wait
        if self.agent_id == greatest_id_junction: return 1

        return self.next_action


    def intention(self, intentions) -> int:
        self.update_information()
        obs = self.split_observations()

        self.next_action = 0

        if self.coords in self.junction_entrance:
            self.calculate_diagonal_square()

            # Entro no cruzamento?
            f_id, _, _ = self.split_square_observation(obs[self.front_square])
            d_id, _, _ = self.split_square_observation(obs[self.diagonal_square])

            self.next_action = 0 if f_id == 0 and d_id == 0 else 1

        elif self.front_square:               # If in game - Only care about cars in front
            f_id, _, _ = self.split_square_observation(obs[self.front_square])
            self.next_action = 0 if f_id == 0 else 1

        next_coords = self.calculate_next_coords(self.next_action)

        intentions[self.agent_id] = (self.coords, next_coords, self.turn_dir, -1)