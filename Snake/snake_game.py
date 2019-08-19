# Flappy Bird
import pygame as pg
import random, time

class Snake:

    def __init__(self, x, y, step, dimensions, screen, length=3, direction=0, head_color=(0,200,0), color=(0,255,0)):

        self.x = x
        self.y = y

        self.length = length
        self.score = 0 # total distance travelled
        self.last_apple = 0
        self.done = False

        self.direction = direction # up, right, down, left
        self.step = step
        self.width, self.height = dimensions
        self.start_positions()

        self.screen = screen
        self.head_color = head_color
        self.color = color

    def start_positions(self):
        # start empty position
        self.positions = []
        # create 'length'* positions
        for i in range(self.length):
            pos = (self.x, self.y + (self.length-i) * self.step)
            self.positions.append(pos)
    
    def change_direction(self, newdirection):

        if newdirection == 0 and self.direction != 2:
            self.direction = 0
        if newdirection == 2 and self.direction != 0:
            self.direction = 2
        if newdirection == 1 and self.direction != 3:
            self.direction = 1
        if newdirection == 3 and self.direction != 1:
            self.direction = 3

    def next_position(self):
        # increment score
        self.score += 1
        # save current position
        self.positions.append((self.x, self.y))
        # next position
        if self.direction == 0:
            self.y -= self.step
        elif self.direction == 1:
            self.x += self.step
        elif self.direction == 2:
            self.y += self.step
        elif self.direction == 3:
            self.x -= self.step
        if len(self.positions) > self.length:
            self.positions.pop(0)

    def draw(self):
        # draw head
        pg.draw.rect(self.screen, self.head_color, (self.x, self.y, self.step, self.step))
        # draw body
        for x,y in self.positions:
            pg.draw.rect(self.screen, self.color, (x,y,self.step,self.step))

    def collide(self):
        if any([(self.x, self.y) == pos for pos in self.positions]):
            self.done = True
        if self.x > self.width - self.step or self.x < 0:
            self.done = True
        if self.y > self.height - self.step or self.y < 0:
            self.done = True
        return self.done

    def is_valid_position(self, position):
        return not position in self.positions or position != (self.x, self.y)

    def direction_vector(self):
        vector = [0,0]
        # edit vector-x or -y
        if self.direction == 0:
            vector[1] -= 1
        elif self.direction == 1:
            vector[0] += 1
        elif self.direction == 2:
            vector[1] += 1
        elif self.direction == 3:
            vector[0] -= 1
        return vector

    def middle_points(self):
        # head + body (inverse, else start at the tail)
        return [(self.x + self.step / 2, self.y + self.step / 2)] + [(position[0] + self.step / 2, position[1] + self.step / 2) for position in self.positions[::-1]]

    def lines(self):
        '''Returns a list of tuples of positions, which are the center of the snake's body 'cubes' '''
        points = self.middle_points()
        lines = [(points[index], points[index+1]) for index in range(len(points)-1)] # optimize the lines, if the snake turned 3 times, there should be max 4 lines, and the length of the snake is not important (réfléchi)
        return lines

    def border_lines(self):
        '''Same as self.lines(), but for the game borders'''
        return [[(0,0), (self.width,0)], [(0,0), (0,self.height)], [(self.width,0), (self.width,self.height)], [(0,self.height), (self.width,self.height)]]





class Apple:

    def __init__(self, apple_width, dimensions, screen, snake):

        self.apple_width = apple_width
        self.width, self.height = dimensions

        self.new_position(snake)

        self.color = (255,0,0)
        self.screen = screen

    def draw(self):
        pg.draw.rect(self.screen, self.color, (self.x, self.y, self.apple_width, self.apple_width))

    def eaten_by(self, snake):
        if (self.x, self.y) == (snake.x, snake.y):
            self.new_position(snake)
            snake.length += 1
            snake.last_apple = snake.score
            return True
    
    def new_position(self, snake):

        new_apple_position = (random.randrange(0,self.width,snake.step), random.randrange(0,self.height,snake.step))
        while snake.is_valid_position(new_apple_position) != True:
            new_apple_position = (random.randrange(0,self.width,snake.step), random.randrange(0,self.height,snake.step))
        self.x, self.y = new_apple_position
    
    def lines(self):
        return [[(self.x,self.y), (self.x+self.apple_width,self.y)], [(self.x,self.y), (self.x,self.y+self.apple_width)], [(self.x+self.apple_width,self.y), (self.x+self.apple_width,self.y+self.apple_width)], [(self.x,self.y+self.apple_width), (self.x+self.apple_width,self.y+self.apple_width)]]


def main():
    global height

    # init pygame
    pg.init()
    pg.display.set_caption('Snake')
    width, height = 800, 500
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()

    # init game data
    snake = Snake(width // 2, height // 2, 10, (width, height), screen)
    apple = Apple(10, (width, height), screen, snake)
    gameOver = False
    FPS = 15

    while not gameOver:

        screen.fill((0,0,0))

        # get user input
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_DOWN and snake.direction != 0:
                    snake.direction = 2
                if event.key == pg.K_UP and snake.direction != 2:
                    snake.direction = 0
                if event.key == pg.K_RIGHT and snake.direction != 3:
                    snake.direction = 1
                if event.key == pg.K_LEFT and snake.direction != 1:
                    snake.direction = 3

            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # do the move
        snake.next_position()
        # check for apple
        apple.eaten_by(snake)

        # check for collisions & score
        gameOver = snake.collide()

        # render
        snake.draw()
        apple.draw()

        # loop end
        pg.display.update()
        clock.tick (FPS)


if __name__ == '__main__':
    main()

