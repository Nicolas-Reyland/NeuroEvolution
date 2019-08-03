# Snake Environment
import snake_game as _fbg
import pygame_utils as _pgu
from numpy import array

import matrix

_fbg.pg.init()

'''
Author: Nicolas Reyland
my github: https://github.com/Nicolas-Reyland
first release on ??/??/????
version: 1.0.0


This module is a personal open-source project
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

        # pygame + game borders
        self.screen = None
        self.width, self.height = 800, 500

        # save
        self.score_till_save = 100

    def init_pygame(self):
        # init pygame
        _fbg.pg.display.set_caption('Snake')
        self.screen = _fbg.pg.display.set_mode((self.width, self.height))
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

        return agent.snake.done

    def observation(self, agent, flatten=True):

        '''
        ob = [[.0 for y in range(0,agent.height,agent.snake.step)] for x in range(0,agent.width,agent.snake.step)]
        for index_x, x in enumerate(range(0,agent.width,agent.snake.step)):
            for index_y, y in enumerate(range(0,agent.height,agent.snake.step)):
                if (x,y) in agent.snake.positions or (x,y) == (agent.snake.x,agent.snake.y):
                    ob[index_x][index_y] = 1.0
                elif (x,y) == (agent.apple.x,agent.apple.y):
                    ob[index_x][index_y] = -1.0

        if flatten: ob = [e for l in ob for e in l]

        return ob
        '''
        observations = []
        for angle in range(0,360,45):
            teta = matrix.deg_to_rad(angle)
            ob = _angle_observation(agent, teta)
            ob = _normalize_observation(ob, agent)
            observations.append(ob)
        return observations

    def render(self):
        if self.pg_active:
            self.screen.fill((0,0,0))
            for agent in self.agents:
                if not agent.snake.done:
                    agent.snake.draw()
                    agent.apple.draw()
        else:
            self.init_pygame()
            self.render()
            return
        # update screen
        _fbg.pg.display.update()
        # check for pygame quit
        for event in _fbg.pg.event.get():
            if event.type == _fbg.pg.QUIT:
                _fbg.pg.quit()
                quit()
    
    def get_clone_info(self):
        return [self.nn_structure, self.width, self.height]

    def clone_to(self, info):

        self.nn_structure = info[0]
        self.width = info[1]
        self.height = info[2]

def _angle_observation(agent, teta):

    # check if lines are parallel (no intersection...)
    if matrix.slope(line[0], line[1]) == matrix.slope(position, position2):
        print('line & position-line are parallel')
        continue

    # coordinates
    x1,y1 = position
    x2,y2 = position2
    x3,y3 = line[0]
    x4,y4 = line[1]
    # intersection point calculation
    px = ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
    py = ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
    # intersection coordinates
    intersection = (px,py)
    print(f'intersection at {intersection}')


def _normalize_observation(ob, agent):
    pass



