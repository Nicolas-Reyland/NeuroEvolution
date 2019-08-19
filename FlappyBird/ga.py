# Genetic Algorithm
from flappy_bird_game import Bird
import numpy as np
import nn

class Agent:
    
    def __init__(self, id, nn_structure, height, screen):

        self.id = id
        self.fitness = 0

        self.height = height
        self.screen = screen
        self.bird = Bird(40, self.height//2, height, self.screen)

        self.nn_structure = nn_structure
        self.brain = nn.NeuralNetwork(nn_structure)

    def predict(self, input_):
        prediction = self.brain.predict(input_)[0]
        #print(1, prediction)
        prediction = round(prediction)
        #print(2, prediction)
        return prediction

    def clone(self):

        clone = Agent(self.id, self.nn_structure, self.height, self.screen)
        clone.brain = self.brain.clone()

        return clone


def build_generation(n, env):

    agents = [Agent(id, env.nn_structure, env.height, env.screen) for id in range(n)]
    return agents

def next_generation(agents):

    # calculate fitness
    fitness_sum = sum([agent.bird.distance for agent in agents])
    for agent in agents:
        agent.fitness = agent.bird.distance / fitness_sum

    # new generation
    population = len(agents)
    agents_backup = agents[:]
    best_agent = list(sorted(agents, key=lambda agent: agent.bird.distance, reverse=True))[0]
    for i in range(population-1):
        agents[i] = pick_one(agents_backup)
    agents[population-1] = best_agent.clone()
    agents[population-1].color = (255,255,0) # doesn't work ?

    return agents

def pick_one(agents):

    index = 0
    r = np.random.random()

    while r > 0:
        r -= agents[index].fitness
        index += 1
    index -= 1

    agent = agents[index]
    child = Agent(agent.id, agent.nn_structure, agent.height, agent.screen)
    child.brain = agent.brain.clone()
    child.brain.mutate(.05)

    return child

def load_agent(s, env):

    weights = np.load(f'saved models/{s} - weights.npy', allow_pickle=True)
    bias = np.load(f'saved models/{s} - bias.npy', allow_pickle=True)
    info = np.load(f'saved models/{s} - info.npy', allow_pickle=True)

    agent = Agent(0, info[0], info[1], None)
    agent.brain.weights = weights[:]
    agent.brain.bias = bias[:]

    env.clone_to(info)

    return agent

