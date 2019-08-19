# Genetic Algorithm
from snake_game import Snake, Apple
import numpy as np
import nn

class Agent:

    def __init__(self, id_, nn_structure, width, height, screen, step=10, length=3):

        self.id = id_
        self.fitness = 0

        self.width = width
        self.height = height

        self.screen = screen
        # randomize snake position / direction ?
        self.snake = Snake(self.width//2, self.height//2, step, (self.width, self.height), self.screen, length=length)
        self.apple = Apple(step, (self.width, self.height), self.screen, self.snake)
        self.base_length = length

        self.nn_structure = nn_structure
        self.brain = nn.NeuralNetwork(nn_structure)
        self.saved = False

    def predict(self, input_):
        prediction = self.brain.predict(input_)
        prediction = np.argmax(prediction) # returns an index
        return prediction

    def get_fitness(self):
        '''Does NOT return the self.fitness. It returns the result of "(self.snake.length - self.base_length + 1) * self.snake.score - (some malus for not eatng apples)"'''
        score = (self.snake.length - self.base_length + 1) * self.snake.score
        if self.snake.score - self.snake.last_apple > 100:
            score -= self.snake.score - self.snake.last_apple / 2
        if self.snake.score - self.snake.last_apple > 1000:
            score -= self.snake.score - self.snake.last_apple * 1.01
        return score

    def clone(self):

        clone = Agent(self.id, self.nn_structure, self.width, self.height, self.screen)
        clone.brain = self.brain.clone()

        return clone


def build_generation(n, env, **kwargs):

    agents = [Agent(id_, env.nn_structure, env.width, env.height, env.screen, **kwargs) for id_ in range(n)]
    return agents

def next_generation(agents, mutate_prob):

    # calculate fitness
    fitness_sum = sum([(agent.snake.length + 1) * agent.snake.score for agent in agents])
    for agent in agents:
        agent.fitness = (agent.snake.length + 1) * agent.snake.score / fitness_sum

    # new generation
    population = len(agents)
    agents_backup = agents[:]
    best_agent = list(sorted(agents, key=lambda agent: agent.get_fitness(), reverse=True))[0]
    for i in range(population-1):
        agents[i] = pick_one(agents_backup, mutate_prob)
    agents[population-1] = best_agent.clone()

    return agents

def pick_one(agents, mutate_prob):

    index = 0
    r = np.random.random()

    while r > 0:
        r -= agents[index].fitness
        index += 1
    index -= 1

    agent = agents[index]
    child = Agent(agent.id, agent.nn_structure, agent.width, agent.height, agent.screen)
    child.brain = agent.brain.clone()
    child.brain.mutate(mutate_prob)

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

