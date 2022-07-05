import argparse, json
import numpy as np
from gym import Env
from typing import Sequence

from aasma import Agent

from traffic.traffic_junction import TrafficJunction

from agents.random import RandomAgent
from agents.greedy import GreedyAgent
from agents.cautious import CautiousAgent
from agents.decent import DecentAgent

import time

def run_multi_agent(environment: Env, agents: Sequence[Agent], n_episodes: int, visualize: bool) -> np.ndarray:

    results = []
    collisions_with = np.zeros(n_episodes)
    collisions = []
    blocked = np.zeros(n_episodes)

    for episode in range(n_episodes):

        steps = 0
        terminals = [False for _ in range(len(agents))]
        observations = environment.reset()

        intentions = {}

        for agent in agents:
            agent.reset()
            intentions[agent.agent_id] = None

        collision_counter = 0

        while not all(terminals):
            steps += 1

            # Visualize the environment
            if visualize:
                environment.render()
                time.sleep(0.1)

            actions = []
            for id, agent in enumerate(agents):
                agent.see(observations[id])
                agent.intention(intentions)
                actions.append(agent.action(intentions))
            obs, _, terminal, info = environment.step(actions)

            observations = obs
            terminals = terminal
            collision_counter += info["step_collisions"]

        if steps < 100:
            results.append(steps)
            collisions.append(collision_counter)
        collisions_with[episode] = collision_counter
        blocked[episode] = 1 if steps >= 100 else 0

        environment.close()

    return np.array(results), np.array(collisions), collisions_with, blocked

def parse_ind_team(teams, data, cars):
    conv = {"R": RandomAgent, "G": GreedyAgent, "C": CautiousAgent, "D": DecentAgent}

    agents = data["agents"]
    c_agents = len(agents)
    name = data["name"]

    teams[name] = [ conv.get( agents[i % c_agents] )(i, cars) for i in range(cars) ]

def parse_teams(team_conf, cars):
    with open("configurations.json") as f:
        teams_def = json.load(f)

    if team_conf not in teams_def: 
        print("ERROR: No configuration found with that name")
        return {}

    teams = {}
    curr = teams_def[team_conf]

    if type(curr) == list:
        for name in curr:
            parse_ind_team(teams, teams_def[name], cars)
    else:
        parse_ind_team(teams, curr, cars)

    return teams

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--episodes", type=int, default=1000)
    parser.add_argument("--cars", type=int, default=10)
    parser.add_argument("--teams", type=str, default="all")
    parser.add_argument("--vis", type=bool, action=argparse.BooleanOptionalAction)
    opt = parser.parse_args()

    # 1 - Setup the environment
    environment = TrafficJunction(n_max=opt.cars)

    # 2 - Setup the teams
    teams = parse_teams(opt.teams, opt.cars)

    # 3 - Evaluate teams
    results = {}
    collisions = {}
    collisions_with = {}
    blocked_r = {}
    for team, agents in teams.items():
        result, n_collisions, n_collisions_with, blocked = run_multi_agent(environment, agents, opt.episodes, opt.vis)
        results[team] = result
        collisions[team] = n_collisions
        collisions_with[team] = n_collisions_with
        blocked_r[team] = np.sum(blocked)

        print(team, np.sum(result) / len(result), np.sum(n_collisions) / len(result), np.sum(n_collisions_with) / opt.episodes, np.sum(blocked))