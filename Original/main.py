import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', ['x', 'y'])

BLOCK_SIZE = 20
SPEED = 10

font = pygame.font.SysFont('arial', 25)

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 106, 187)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
GREEN = (13, 187, 0)


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snakes on the plane")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)

        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x + (2 * BLOCK_SIZE), self.head.y)
                      ]

        self.score = 0
        self.food = None
        self.padLR = 20
        self.padT = 40
        self.padB = 20
        self._place_food()

    # creates the food
    def _place_food(self):
        x = random.randint(self.padLR, self.w - (self.padLR * 2)) // BLOCK_SIZE * BLOCK_SIZE
        y = random.randint(self.padT, self.h - (self.padT + self.padB)) // BLOCK_SIZE * BLOCK_SIZE
        self.food = Point(x, y)
        # Ensure food is not in snake occupied path
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # user input

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # error check if direction click is not opposite
                    if self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT

                elif event.key == pygame.K_RIGHT:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT

                elif event.key == pygame.K_UP:
                    if self.direction != Direction.DOWN:
                        self.direction = Direction.UP

                elif event.key == pygame.K_DOWN:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN

        # Moving

        self._move(self.direction)
        self.snake.insert(0, self.head)

        # Check if game is done
        game_over = False

        if self._is_collision():
            game_over = True
            return game_over, self.score

        # food stuff
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self.snake.insert(0, self.head)
            # for i in range(20):
            #     self.snake.insert(0, self.head)

        else:
            self.snake.pop()

        self._update_ui()

        self.clock.tick(SPEED)

        # returns game overs

        return game_over, self.score

    def _is_collision(self):
        # hit the wall

        # Adjust for playable area

        if self.head.x > self.w - 40 \
                or self.head.x < 20 \
                or self.head.y > self.h - 40 \
                or self.head.y < 40:
            return True
            # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

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
        pygame.display.flip()

    def endScreen(self):
        # Sets a translucent gray overlay on top of the game window.
        trans = pygame.Surface((self.w, self.h))
        trans.set_alpha(100)
        trans.fill(BLACK)
        self.display.blit(trans, (0, 0))

        # Displays the "GAME OVER" text.
        text = font.render("GAME OVER Score:" + str(self.score), True, WHITE)
        text_rect = text.get_rect(center=(self.w // 2, self.h // 2 - BLOCK_SIZE // 2))
        self.display.blit(text, text_rect)
        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGame()

    while True:

        game_over, score = game.play_step()

        if game_over:
            game.endScreen()
            waiting_for_key = True
            while waiting_for_key:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    elif event.type == pygame.KEYDOWN:
                        waiting_for_key = False

            break


    print('Final score:', score)

    pygame.quit()
