# Genetic Algorithm
from snake_game import Snake, Apple
import numpy as np
import nn

class Agent:

    def __init__(self, id_, nn_structure, width, height, screen, step=10):

        self.id = id_
        self.fitness = 0

        self.width = width
        self.height = height

        self.screen = screen
        # randomize snake position / direction ?
        self.snake = Snake(self.width//2, self.height//2, step, (self.width, self.height), self.screen)
        self.apple = Apple(step, (self.width, self.height), self.screen, self.snake)

        self.nn_structure = nn_structure
        self.brain = nn.NeuralNetwork(nn_structure)

    def predict(self, input_):
        prediction = self.brain.predict(input_)
        prediction = np.argmax(prediction) # returns an index
        return prediction

    def clone(self):

        clone = Agent(self.id, self.nn_structure, self.width, self.height, self.screen)
        clone.brain = self.brain.clone()

        return clone


def build_generation(n, env):

    agents = [Agent(id_, env.nn_structure, env.width, env.height, env.screen) for id_ in range(n)]
    return agents

def next_generation(agents):

    # calculate fitness
    fitness_sum = sum([agent.snake.length for agent in agents])
    for agent in agents:
        agent.fitness = agent.snake.length / fitness_sum

    # new generation
    population = len(agents)
    agents_backup = agents[:]
    best_agent = list(sorted(agents, key=lambda agent: agent.snake.length, reverse=True))[0]
    for i in range(population-1):
        agents[i] = pick_one(agents_backup)
    agents[population-1] = best_agent.clone()

    return agents

def pick_one(agents):

    index = 0
    r = np.random.random()

    while r > 0:
        r -= agents[index].fitness
        index += 1
    index -= 1

    agent = agents[index]
    child = Agent(agent.id, agent.nn_structure, agent.width, agent.height, agent.screen)
    child.brain = agent.brain.clone()
    child.brain.mutate(.05)

    return child

def load_agent(s, env):

    weights = np.load(f'saved models/{s} - weights.npy', allow_pickle=True)
    bias = np.load(f'saved models/{s} - bias.npy', allow_pickle=True)
    info = np.load(f'saved models/{s} - info.npy', allow_pickle=True)

    agent = Agent(0, info[0], info[1], info[2], None)
    agent.brain.weights = weights[:]
    agent.brain.bias = bias[:]

    env.clone_to(info)

    return agent

