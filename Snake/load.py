# Enviroenment Flappy Bird NeuroEvolution
from snake import make
from ga import load_agent
import sys


population = 1000
env = make([25,16,4])

agent = load_agent(sys.argv[1], env)

env.reset()

env.agents = [agent]

while not agent.snake.done:
    info = env.observation(agent)
    next_move = agent.predict(info)
    env.step(agent, next_move)
    # render the game
    env.render(agent)

print('finished with score: {}'.format(env.best_score))

