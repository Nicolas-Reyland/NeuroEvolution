# Flappy Bird
import pygame as pg
import random, time

class Bird:

    def __init__(self, x, y, game_height, screen):

        self.x = x
        self.y = y
        self.neg = 1

        self.width = 20
        self.game_height = game_height

        self.score = 0
        self.distance = 0
        self.done = False

        self.last_jumped = 0
        self.jumpCount = 0
        self.isJump = False

        self.constrain_jump = False

        self.screen = screen
        self.color = (255,0,0)

    def next_position(self):
        neg = 1
        if self.jumpCount < 0:
            neg = -1
        self.y -= self.jumpCount**2 * neg * .15
        self.jumpCount -= 1
        self.distance += 1

    def jump(self):
        if self.constrain_jump:
            if self.jumpCount <= 3: # can only jump if moving down (or still ?)
                self.jumpCount = 10
        else:
            self.jumpCount = 10


    def draw(self):
        #pg.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.width)
        pg.draw.rect(self.screen, self.color, (int(self.x)-self.width//2, int(self.y)-self.width//2, self.width, self.width))

    def collide(self, pipe):
        # stick to the roof
        self.y = 0 if self.y < self.width // 2 else self.y
        # collision with the floor
        if self.y > self.game_height:
            return True
        # collision with a pipe
        for corner in [(self.x-self.width//2, self.y-self.width//2), (self.x+self.width//2, self.y-self.width//2), (self.x+self.width//2, self.y-self.width//2), (self.x+self.width//2, self.y+self.width//2)]:
            if pipe.x <= corner[0] <= pipe.x + pipe.pipe_width and 0 <= corner[1] <= pipe.y:
                return True
            if pipe.x <= corner[0] <= pipe.x + pipe.pipe_width and pipe.y + pipe.gap <= corner[1] <= pipe.height:
                return True
        return False





class Pipe:

    def __init__(self, x, screen, pipe_width, height, gap, speed, between_pipe_gap, max_height_gap):

        self.x = x
        self.y = random.randrange(10, height - gap - 10)

        self.pipe_width = pipe_width
        self.between_pipe_gap = between_pipe_gap
        self.gap = gap
        self.max_height_gap = max_height_gap
        self.marked = False

        self.speed = speed
        self.height = height

        self.screen = screen
        self.color = (255,255,255)

    def draw(self):
        pg.draw.rect(self.screen, self.color, (self.x, 0, self.pipe_width, self.y))#(self.x, 0, self.x + self.pipe_width, self.y - self.gap))
        pg.draw.rect(self.screen, self.color, (self.x, self.y + self.gap, self.pipe_width, self.height))

    def move(self):
        self.x -= self.speed

    def been_passed(self, bird):
        if not self.marked:
            if self.x + self.pipe_width // 2 <= bird.x:
                self.marked = True
                return True


def generate_pipes(screen, pipe_width, height, gap, speed, between_pipe_gap, max_height_gap):

    pipes = [Pipe(x, screen, pipe_width, height, gap, speed, between_pipe_gap, max_height_gap)
             for x in range(400, 400 + between_pipe_gap * 5, between_pipe_gap)]

    control_pipe_height(pipes, max_height_gap)

    return pipes


def control_pipe_height(pipes, max_height_gap):

    last_pipe = pipes[0]
    for pipe in pipes[1:]:
        if last_pipe.y - pipe.y > max_height_gap:
            pipe.y = last_pipe.y - max_height_gap
        elif pipe.y - last_pipe.y > max_height_gap:
            pipe.y = last_pipe.y + max_height_gap

def new_pipes(pipes):

    for pipe in pipes:
        if pipe.x + pipe.pipe_width < 0:
            pipe.x = max([pipe.x for pipe in pipes]) + pipe.pipe_width + pipe.between_pipe_gap
            pipe.marked = False
            break
    
    control_pipe_height(pipes, pipes[0].max_height_gap)



def main():
    global height

    # init pygame
    pg.init()
    pg.display.set_caption('Flappy Bird')
    width, height = 800, 500
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()

    # init game data
    bird = Bird(40, 10, height, screen)
    pipe_width = 75
    gap = 100
    speed = 7
    between_pipe_gap = 250
    max_height_gap = 200
    pipes = generate_pipes(screen, pipe_width, height, gap, speed, between_pipe_gap, max_height_gap)
    gameOver = False
    FPS = 15

    while not gameOver:

        screen.fill((0,0,0))

        # get user input
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bird.jump()
                if event.key == pg.K_t:
                    bird.isJump = False
                
                if event.key == pg.K_DOWN:
                    bird.y += 10
                if event.key == pg.K_UP:
                    bird.y -= 10
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # do the move
        bird.next_position()
        for pipe in pipes:
            pipe.move()

        # check for collisions & score
        for pipe in pipes:
            if bird.collide(pipe):
                gameOver = True
                break
            if pipe.been_passed(bird):
                bird.score += 1

        # generate new pipes (move old pipes)
        new_pipes(pipes)

        # render
        for pipe in pipes:
            pipe.draw()
        bird.draw()

        # loop end
        pg.display.update()
        clock.tick (FPS)

        print('velocity : ', bird.jumpCount)


if __name__ == '__main__':
    main()

