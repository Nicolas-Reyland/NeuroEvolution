# Enviroenment Flappy Bird NeuroEvolution
from flappy_bird import make
from ga import load_agent
import sys

population = 1000
nn_structure = [5, 5, 1]
env = make(nn_structure)
use_custom = False # make this with the loading agent

agent = load_agent(sys.argv[1], env)

env.reset()
if use_custom:
    print('using custom pipe config')
    env.gap = 150
    env.between_pipe_gap = 400
    env._gen_pipes()

env.agents = [agent]

while not agent.bird.done:
    info = env.observation(agent)
    next_move = agent.predict(info) # move is 0 or 1 (nothing or jump)
    done = env.step(agent, next_move)
    # big step in game
    env.update()
    # render the game
    env.render()

print('finished with score: {}'.format(env.best_score))
print(agent.bird.score)

