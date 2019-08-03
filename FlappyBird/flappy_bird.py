# Flappy Bird Environment
import flappy_bird_game as _fbg
import pygame_utils as _pgu
from numpy import array

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
    This environment simulates the Flappy Bird Game
    (it is an imitation of gym-library environments)

    """
    ### ----- environment initialisation -----
    def __init__(self, nn_structure):

        self.agents = []
        self.nn_structure = nn_structure

        self.pg_active = False
        self.clock = _fbg.pg.time.Clock()

        # pygame + game borders
        self.screen = None
        self.width, self.height = 800, 500

        # save
        self.score_till_save = 100

    def init_pygame(self):
        # init pygame
        _fbg.pg.display.set_caption('Flappy Bird')
        self.screen = _fbg.pg.display.set_mode((self.width, self.height))
        # pass screen
        for agent in self.agents:
            agent.bird.screen = self.screen
        for pipe in self.pipes:
            pipe.screen = self.screen
        # pygame utils
        _pgu.screen = self.screen
        _pgu.disp_w, _pgu.disp_h = self.width, self.height
        self.pg_active = True

    def reset(self):
        # init game data
        self.pipe_width = 75
        self.gap = 100
        self.speed = 7
        self.between_pipe_gap = 250
        self.max_height_gap = 200
        self._gen_pipes()
        self.gameOver = False
        self.FPS = 15
        self.next_pipe = self.pipes[0]
        self.pg_active = False
        self.best_score = 0
    
    def _gen_pipes(self):
        self.pipes = _fbg.generate_pipes(self.screen, self.pipe_width, self.height, self.gap, self.speed, self.between_pipe_gap, self.max_height_gap)

    def step(self, agent, move):
        assert agent in self.agents
        assert self.agents
        assert not agent.bird.done

        if move == 1:
            agent.bird.jump()
 
        agent.bird.next_position()

        for pipe in self.pipes:
            if agent.bird.collide(pipe):
                agent.bird.done = True
                break

        return agent.bird.done

    def update(self):
        for pipe in self.pipes:
            pipe.move()
        # generate new pipes
        _fbg.new_pipes(self.pipes)
        # choose next pipe here
        pipes = list(filter(lambda pipe: pipe.x + pipe.pipe_width > self.agents[0].bird.x, self.pipes))
        pipes = list(sorted(pipes, key=lambda pipe: pipe.x))
        self.next_pipe = pipes[0]
        # check for bird achievements
        for agent in self.agents:
            if self.next_pipe.been_passed(agent.bird):
                self.best_score += 1
                break
        # colorate the next pipe
        for p in self.pipes:
            p.color = (255,255,255)
        self.next_pipe.color = (255,0,0)
        # stop at certain score
        if self.best_score == self.score_till_save:
            for agent in self.agents:
                if not agent.bird.done:
                    agent.brain.save(self)
                    print('saved')
                    break
            else:
                raise ValueError('No agent with score 100 ...')

    def observation(self, agent):
        return array([agent.bird.y / self.height, self.next_pipe.y / self.height, (self.next_pipe.y + self.next_pipe.gap) / self.height, self.next_pipe.x / self.width, agent.bird.jumpCount / 30]) # min velocity is -26, and max is 9

    def render(self):
        if self.pg_active:
            self.screen.fill((0,0,0))
            for pipe in self.pipes:
                pipe.draw()
            for agent in self.agents:
                if not agent.bird.done:
                    agent.bird.draw()
        else:
            self.init_pygame()
            self.render()
            return
        # best score
        if self.pg_active:
            for agent in self.agents:
                if not agent.bird.done:
                    _pgu.message_to_screen(str(self.best_score), (0,255,0), -200, size='medium')
                    break
        # update screen
        _fbg.pg.display.update()
        # check for pygame quit
        for event in _fbg.pg.event.get():
            if event.type == _fbg.pg.QUIT:
                _fbg.pg.quit()
                quit()
    
    def get_clone_info(self):
        return [self.nn_structure, self.height, self.pipe_width, self.gap, self.speed, self.between_pipe_gap, self.max_height_gap]

    def clone_to(self, info):

        self.nn_structure = info[0]
        self.height = info[1]
        self.pipe_width = info[2]
        self.gap = info[3]
        self.speed = info[4]
        self.between_pipe_gap = info[5]
        self.max_height_gap = info[6]





