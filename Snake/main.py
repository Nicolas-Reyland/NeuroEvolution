# Enviroenment Flappy snake NeuroEvolution
from snake import make
import ga

population = 1
render_after_gen = 0
do_render = True
nn_structure = [800 * 500 // 10, (800 * 500 // 2) // 10, 4]
env = make(nn_structure)
use_custom = False

generations = 0

while True:

    print(f'[!] Starting Generation: {generations}')

    all_done = False
    env.reset()

    agents = ga.build_generation(population, env) # n agents
    env.agents = agents

    for agent in agents:
        while not agent.done:
            info = env.observation(agent)
            next_move = agent.predict(info)
            done = env.step(agent, next_move)
            # render the game
            if generations >= render_after_gen and do_render:
                env.render()

    print('[s] best score: {}'.format(env.best_score))

    generations += 1

    if generations == 50:
        print('[!!] RESETING ALL')
        agents = ga.build_generation(population, env) # n agents
        generations = 0
    else:
        # do nn studd here ...
        agents = ga.next_generation(agents)



