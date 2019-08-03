# Enviroenment Flappy Bird NeuroEvolution
from flappy_bird import make
import ga

population = 1000
render_after_gen = 0
do_render = True
nn_structure = [5, 5, 1]
env = make(nn_structure)
use_custom = False

agents = ga.build_generation(population, env) # n agents
generations = 0

while True:

    print(f'[!] Starting Generation: {generations}')

    all_done = False
    env.reset()
    env.max_height_gap = 350
    if use_custom:
        env.gap = 150
        env.between_pipe_gap = 400
        env._gen_pipes()

    env.agents = agents

    while not all_done:
        for i,agent in enumerate(agents):
            info = env.observation(agent)
            if not agent.bird.done:
                next_move = agent.predict(info) # move is 0 or 1 (nothing or jump)
                done = env.step(agent, next_move)
        # big step in game
        env.update()
        # render the game
        if generations >= render_after_gen and do_render:
            env.render()
        # at least one agent alive
        all_done = all([agent.bird.done for agent in agents])

    print('[s] best score: {}'.format(env.best_score))

    generations += 1

    if generations == 50:
        print('[!!] RESETING ALL')
        agents = ga.build_generation(population, env) # n agents
        generations = 0
    else:
        # do nn studd here ...
        agents = ga.next_generation(agents)




