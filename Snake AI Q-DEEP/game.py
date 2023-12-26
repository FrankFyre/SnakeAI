import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 106, 187)
BLACK = (0,0,0)
GREY = (100,100,100)
GREEN = (13, 187, 0 )

BLOCK_SIZE = 20
SPEED = 300


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('AI Snake')
        self.clock = pygame.time.Clock()
        self.current_game = 0
        self.padLR = 20
        self.padT = 40
        self.padB = 20
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self.current_game += 1
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(self.padLR, self.w - (self.padLR * 2)) // BLOCK_SIZE * BLOCK_SIZE
        y = random.randint(self.padT, self.h - (self.padT + self.padB)) // BLOCK_SIZE * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        #  pygame run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Snake move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # Game over check
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Check if eaten and replace food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # update snake on screen ui
        self._update_ui()
        self.clock.tick(SPEED)
        #  return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - 40 or pt.x < 20 or pt.y > self.h - 40 or pt.y < 40:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        # draw border
        # borderwidth used for adjusted in play area
        bWidth = 1
        pygame.draw.rect(self.display, GREY,
                         (self.padLR - bWidth, self.padT - bWidth, self.w - self.padT + bWidth, self.h -
                          (self.padT + self.padB) + bWidth), width=bWidth)

        r = 255
        g = 216
        b = 0
        gradient = 0

        for i, pt in enumerate(self.snake):
            finalcolor = (r, max(g - gradient, 0), b)  # Ensure finalG does not go below 0
            pygame.draw.rect(self.display, BLACK, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

            if i == 0:  # Head of the snake
                pygame.draw.rect(self.display, finalcolor, pygame.Rect(pt.x + 0.1, pt.y + 0.1, 19, 19))
            else:
                # For the body segments, make them darker
                pygame.draw.rect(self.display, finalcolor,
                                 pygame.Rect(pt.x + 0.1, pt.y + 0.1, 19, 19))
            spread = len(self.snake)
            gradient += (g / spread)

        pygame.draw.rect(self.display, BLUE, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [20, 5])

        game_number_text = font.render("Game: " + str(self.current_game), True, WHITE)
        self.display.blit(game_number_text, [self.w - 120, 5])

        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  #turn Right
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # turn left

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)