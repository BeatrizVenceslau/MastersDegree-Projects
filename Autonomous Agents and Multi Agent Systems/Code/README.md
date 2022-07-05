# Autonomous Agents & Multi-Agent Systems
### IST, Spring Semester 2022

### Quickstart

1. Create virtual environment
    
    ```
    $ python3 -m venv venv
    ```
    ```
    $ source venv/bin/activate
    ```

2. Install dependencies
    
    ```
    $ pip install -r requirements.txt
    ```


3. Run the simulation

    The simulation can be run with the following command:

    ```
    $ python run_simulation.py [--episodes EPISODES] [--cars CARS] [--teams TEAMS] [--vis]
    ```

    **EPISODES** (number of episodes of each simulation)  
    Default: 1000

    **CARS** (number of cars in each simulation)  
    Default: 10  
    Can be any value between 1 and 10 (inclusive)

    **TEAMS** (team or set of teams that will be runned)  
    Default: all
    Options:
    * random
    * greedy
    * cautious
    * decent
    * greedy+cautious
    * greedy+decent
    * cautious+decent
    * single - will run (random, greedy, cautious and decent)
    * multi - will run (greedy+cautious, greedy+decent, cautious+decent)
    * all - will run all of the first 7 options

    **--vis** (if this flag is added to the command, it is possible to see the visualization)