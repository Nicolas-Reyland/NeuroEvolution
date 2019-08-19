# Enviroenment Flappy snake NeuroEvolution
from __future__ import print_function
from snake import make
import ga

population = 1000
render_after_gen = 0
do_render = False
nn_structure = [24,16,4]
env = make(nn_structure)

print('[ ! ] Population: {} NeuralNetwork Structure: {} rendering: {} [ ! ]'.format(population, nn_structure, do_render))

fitness_list = []

generations = 0
while True:

    print('[!] Starting Generation: {}{}['.format(generations, ' ' * (3 - len(str(generations)))), end='')

    all_done = False
    env.reset()

    agents = ga.build_generation(population, env, **{'length': 10}) # n agents
    env.agents = agents

    for i,agent in enumerate(agents):
        # print('[a] Agent {}'.format(agent.id))
        while not agent.snake.done:
            info = env.observation(agent)
            next_move = agent.predict(info)
            done = env.step(agent, next_move)
            # render the game
            if generations >= render_after_gen and do_render:
                env.render(agent)

        if i % (population // 20) == 0: print('*', end='', flush=True)

    print(']', end='')

    print(' , best score: {}'.format(env.best_score))
    fitness_list.append(ga.np.mean([agent.get_fitness() for agent in env.agents]))

    generations += 1

    # do nn studd here ...
    agents = ga.next_generation(agents, .1)



