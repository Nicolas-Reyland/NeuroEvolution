# Snake Environment
import snake_game as _sg
import pygame_utils as _pgu
from numpy import array
from observation_functions import *

import matrix

_sg.pg.init()

'''
Author: Nicolas Reyland
my github: https://github.com/Nicolas-Reyland
first release on ??/??/????
version: 1.0.0

This is a personal open-source project
It contains a snake-game environment. The environment is made to look
the same as openai environments.

Check out openai here: https://github.com/openai
#I personally recommand you the gym and retro repos

For this module, you will need the python-modules in requirements.txt
To install all the modules, open a terminal/cmd, go to the repo folder
and type: 'pip install -r requirements.txt'

If you read this, you can skip the README.md


Global Notes:
 - if you have any issue, tell me on github


'''

def make(nn_structure):
    return env(nn_structure)

# ---------------------------------------------------------------- #
#                         Main Env Class                           #
# ---------------------------------------------------------------- #
class env(object):
    """
    This environment simulates the Snake Game
    (it is an imitation of gym-library environments)

    """
    ### ----- environment initialisation -----
    def __init__(self, nn_structure):

        self.agents = []
        self.nn_structure = nn_structure

        self.pg_active = False
        self.angle_step = 45

        # pygame + game borders
        self.screen = None
        self.width, self.height = 800, 500

        # save
        self.score_till_save = 5000

    def init_pygame(self):
        # init pygame
        _sg.pg.display.set_caption('Snake')
        self.screen = _sg.pg.display.set_mode((self.width, self.height))
        # pass screen
        for agent in self.agents:
            agent.snake.screen = self.screen
            agent.apple.screen = self.screen
        # pygame utils
        _pgu.screen = self.screen
        _pgu.disp_w, _pgu.disp_h = self.width, self.height
        self.pg_active = True

    def reset(self):
        # init game data
        self.pg_active = False
        self.best_score = 0

    def step(self, agent, move):
        assert agent in self.agents
        assert self.agents
        assert not agent.snake.done

        agent.snake.change_direction(move)
        agent.snake.next_position()
        agent.snake.collide()

        agent.apple.eaten_by(agent.snake)
        if agent.get_fitness() > self.best_score:
            self.best_score = agent.get_fitness()
        
        if agent.get_fitness() >= self.score_till_save and not agent.saved:
            agent.brain.save(self)
            agent.saved = True

        if agent.snake.score - agent.snake.last_apple > 500:
            agent.snake.done = True

        return agent.snake.done

    def observation(self, agent):

        observation = []
        for angle in range(0,360,self.angle_step):

            teta = matrix.deg_to_rad(angle)
            ob = try_angle_observation(agent, agent.snake.lines(), teta)
            observation.append(ob)

        for angle in range(0,360,self.angle_step):

            teta = matrix.deg_to_rad(angle)
            ob = angle_observation(agent, agent.snake.border_lines(), teta)
            observation.append(ob)

        for angle in range(0,360,self.angle_step):

            teta = matrix.deg_to_rad(angle)
            ob = try_angle_observation(agent, agent.apple.lines(), teta)
            observation.append(ob)

        observation = normalize_observation(agent, observation)
        # observation.append(angle_with_apple(agent))

        # print(f'observation: {observation}')

        return observation

    def render(self, agent):
        if self.pg_active:
            self.screen.fill((0,0,0))
            if not agent.snake.done:
                agent.snake.draw()
                agent.apple.draw()
        else:
            self.init_pygame()
            self.render(agent)
            return
        # update screen
        _sg.pg.display.update()
        # check for pygame quit
        for event in _sg.pg.event.get():
            if event.type == _sg.pg.QUIT:
                _sg.pg.quit()
                quit()
        _sg.pg.display.update()

    def render_observation(self, agent, observation):

        for i,coord in enumerate(observation):
            # full white is 1st
            _sg.pg.draw.line(self.screen, [255 - 255 / len(observation) * i]*3, agent.snake.middle_points()[0], coord, 1)
            # print('[!!] DRAWN LINE')
        _sg.pg.display.update()

    def get_clone_info(self):
        return [self.nn_structure, self.width, self.height]

    def clone_to(self, info):

        self.nn_structure = info[0]
        self.width = info[1]
        self.height = info[2]



