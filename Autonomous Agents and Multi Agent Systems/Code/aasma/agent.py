import numpy as np
from abc import ABC, abstractmethod


class Agent(ABC):

    """
    Base agent class.
    Represents the concept of an autonomous agent.

    Attributes
    ----------
    name: str
        Name for identification purposes.
        
    observation: np.ndarray
       The most recent observation of the environment


    Methods
    -------
    see(observation)
        Collects an observation

    action(): int
        Abstract method.
        Returns an action, represented by an integer
        May take into account the observation (numpy.ndarray).

    References
    ----------
    ..[1] Michael Wooldridge "An Introduction to MultiAgent Systems - Second
    Edition", John Wiley & Sons, p 44.


    """

    def __init__(self, name: str, n_agents: int, agent_id):
        """
        Initialize the agent
        """
        
        self.agent_id = agent_id
        self.name = name
        self.n_agents = n_agents

        self.coords = None
        self.turn_dir = None
        self.diagonal_square = None

        self.observation = None
        self.vector = None
        self.front_square = None
        self.turning_square = None
        self.turned = False

    def reset(self):
        """
        Reset variables
        """

        self.coords = None
        self.turn_dir = None
        self.diagonal_square = None

        self.observation = None
        self.vector = None
        self.front_square = None
        self.turning_square = None
        self.turned = False

    def split_observations(self):
        """
        Split the full observation into the 9 squares of vision
        """

        dx = len(self.observation)//9
        return [self.observation[i*dx : i*dx + dx] for i in range(9)]

    def split_square_observation(self, obs):
        """
        Split the square observation into usable values
        """

        _id = obs[ : self.n_agents]
        coords = obs[self.n_agents : self.n_agents + 2]
        dir = obs[self.n_agents + 2 :]

        _id = np.argmax(_id) + 1 if np.any(_id) else 0

        return _id, list(coords), np.argmax(dir)

    def see(self, observation: np.ndarray):
        """
        Get the observation
        """

        self.observation = observation

    def calculate_direction(self, coords):
        """
        Calculate the direction that the agent is moving when it starts
        """
        
        if coords[0] == 13: self.vector = (-1, 0) #bottom
        if coords[0] == 0: self.vector = (1, 0)   #top
        if coords[1] == 0: self.vector = (0, 1)   #left
        if coords[1] == 13: self.vector = (0, -1) #right

    def update_direction(self, turning_dir):
        """
        After reaching the turning square, update the direction vector
        """
        self.turned = True
        
        if turning_dir == 0: return
        if turning_dir == 1: # Dir
            mult = 1 if self.vector[0] == 0 else -1
            self.vector = (self.vector[1], mult * self.vector[0])
        else: # Esq
            mult = 1 if self.vector[1] == 0 else -1
            self.vector = (mult * self.vector[1], self.vector[0])


    def calculate_turning_square(self, coords, turning_dir):
        """
        Calculate the square where the car will make the turn
        """

        cx, cy = coords
        steps = 7 if turning_dir == 2 else 6
        self.turning_square = [cx + steps * self.vector[0], cy + steps * self.vector[1]]

    def calculate_diagonal_square(self):
        """
        Calculate the observation square in the front-left square of the car 
        """

        if self.vector == (-1, 0): self.diagonal_square = 0
        if self.vector == (1, 0): self.diagonal_square = 8
        if self.vector == (0, 1): self.diagonal_square = 2
        if self.vector == (0, -1): self.diagonal_square = 6

    def calculate_forward_square(self):
        """
        Calculate the observation square in front of the car 
        """

        if self.vector == (-1, 0): self.front_square = 1
        if self.vector == (1, 0): self.front_square = 7
        if self.vector == (0, 1): self.front_square = 5
        if self.vector == (0, -1): self.front_square = 3

    def update_information(self):
        obs = self.split_observations()
        _, self.coords, self.turn_dir = self.split_square_observation(obs[4])

        # If agent is in the game
        if not self.vector and self.coords != [0, 0]:
            self.calculate_direction(self.coords)
            self.calculate_forward_square()
            self.calculate_turning_square(self.coords, self.turn_dir)

        # If agent reached the turning square
        if self.coords == self.turning_square and not self.turned:
            self.update_direction(self.turn_dir)
            self.calculate_forward_square()
            self.calculate_diagonal_square()

        # print(self.name, self.agent_id+1, self.coords, self.turn_dir, self.vector, self.front_square, self.diagonal_square)

    def calculate_next_coords(self, intention):
        if intention or not self.vector: # == 1
            return self.coords
        else:
            return (self.coords[0] + self.vector[0], self.coords[1] + self.vector[1])

    @abstractmethod
    def action(self, intentions) -> int:
        raise NotImplementedError()

    @abstractmethod
    def intention(self, intentions) -> int:
        raise NotImplementedError()