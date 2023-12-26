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

frame_size = 600

BLOCK_SIZE = 20
SPEED = 10

font = pygame.font.SysFont('arial', 25)

w = 32
h = 24

winW = w * BLOCK_SIZE
winH = h * BLOCK_SIZE

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 106, 187)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
GREEN = (13, 187, 0)


class SnakeGame:
    def __init__(self):
        self.w = winW
        self.h = winH
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snakes on the plane")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT

        self.head = Point(self.w // 2, self.h // 2)

        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x + (2 * BLOCK_SIZE), self.head.y)
                      ]

        self.score = 0
        self.food = None
        self.padLR = 0
        self.padT = 0
        self.padB = 0
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
        print("Enter Play step")
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
        newer = generate_move(self.snake, self.food, hamiltonian_cycle(self.snake))
        print("newer")
        print(newer)
        # self.direction = DIRECTION.LEFT

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

        else:
            self.snake.pop()

        self._update_ui()

        self.clock.tick(SPEED)

        # returns game overs

        return game_over, self.score

    def _is_collision(self):
        # hit the wall

        # Adjust for playable area

        if self.head.x > self.w - BLOCK_SIZE \
                or self.head.x < 0 \
                or self.head.y > self.h - BLOCK_SIZE \
                or self.head.y < 0:
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


def get_dir_dict(x, y, x_lim, y_lim):
    adj_dict = dict()
    if y > 0:
        adj_dict[(x, y - 1)] = Direction.UP
    if y < y_lim:
        adj_dict[(x, y + 1)] = Direction.DOWN
    if x > 0:
        adj_dict[(x - 1, y)] = Direction.LEFT
    if x < x_lim:
        adj_dict[(x + 1, y)] = Direction.RIGHT
    return adj_dict


def prims_algorithm():
    # The conn_dict dictionary is assigned all nodes in the guide grid as keys, and an empty array as values. The arrays
    # are gradually filled up with the chosen path of the Minimum Spanning Tree according to Prim's Algorithm

    # The full_dir_dict dictionary is assigned all nodes in the guide grid as keys, and their corresponding "dir_dict"
    # as values (see the get_dir_dict function for an explanation on "dir_dict"s).
    print("prim enter")
    conn_dict, full_dir_dict = dict(), dict()
    for y in range(h // 2):
        for x in range(w // 2):
            conn_dict[(x, y)] = []
            full_dir_dict[(x, y)] = get_dir_dict(x, y, w // 2 - 1, h // 2 - 1)
    start = random.choice(list(full_dir_dict.keys()))  # Picks a node at random to start the MST.
    frontier = list(full_dir_dict[start].keys())  # Lists all available nodes that currently border the MST.
    visited = [start]  # Lists all nodes that have already been visited and are a part of the MST.
    desired_size = (w // 2) * (h // 2)

    # Repeat until all nodes have been visited:
    while len(visited) < desired_size:
        # Picks a random node from within the frontier.
        a = random.choice(frontier)

        available = []
        new_frontier = []

        # Checks all nodes that border the selected node.
        for adj in full_dir_dict[a].keys():
            # If the node has been visited and is a part of the MST, add it as a possible connection.
            if adj in visited:
                available.append(adj)
            # Otherwise, add it to the extended frontier, since it border the tree after the new edge is created.
            elif adj not in frontier:
                new_frontier.append(adj)

        # Pick a random node from the possible connections.
        b = random.choice(available)

        # Add the frontier node to the visited list and add the connection directions to the conn_dict for each of
        # the nodes.
        visited.append(a)
        conn_dict[b].append(full_dir_dict[b][a])
        conn_dict[a].append(full_dir_dict[a][b])

        # Remove the node from the frontier and add the new nodes that border the MST.
        frontier.remove(a)
        frontier += new_frontier
    print(f'exiting prism ')
    return conn_dict


# The hamiltonian_cycle function takes in the current snake object and builds a Hamiltonian Cycle that begins and ends
# at the snake's head. The function uses a Prim's Minimum Spanning Tree with half the dimensions as a guideline to build
# the hamiltonian cycle.
def hamiltonian_cycle(snake):
    # The conn_dict holds the connection of all the Prim's MST nodes.
    print("hamil")
    conn_dict = prims_algorithm()
    cycle = [snake[0]]

    # The cell_dict contains information about a tile's relative position within a cell (MST node).
    cell_dict = dict()
    for y in range(h):
        for x in range(w):
            cell_dict[x, y] = [(x // 2, y // 2), (x % 2, y % 2)]

    # Repeat the cycle contains all tiles in the game grid.
    while len(cycle) < w * h:
        # Selects the current final tile in the cycle.
        print(f'cucle {cycle[-1]}')
        sd = cycle[-1][0]
        xd = cycle[-1][1]
        print ( sd )
        newX = ((sd/10)/2)
        newY = ((xd/10)/2)

        current_tile = Point(newX, newY)

        x, y = current_tile.x, current_tile.y
        print(f'titile {current_tile}')



        # The dir_dict dictionary contains information about the tiles bordering the currently selected tile, and their
        # relative direction to that tile.
        dir_dict = get_dir_dict(x, y, w - 1, h - 1)

        # Selects the cell that contains the currently selected tile.


        current_cell, cell_pos = cell_dict[current_tile]

        cell_conn = conn_dict[current_cell]
        print("FUCK")
        # Repeat for all adjacent tiles that are not already within the cycle:
        for adj_tile in dir_dict.keys():
            if adj_tile not in cycle:
                # adj_conn contains the adjacent tile's relative direction to the selected tile.
                adj_conn = dir_dict[adj_tile]

                # If the adjacent tile is within a different cell to the selected one, and the current cell has a
                # connection to the other cell in the same direction as the selected tile to the adjacent tile,
                # add the adjacent tile to the cycle.
                if current_cell != cell_dict[adj_tile][0]:
                    if adj_conn in cell_conn:
                        cycle.append(adj_tile)
                        break

                # Otherwise if the adjacent tile is within the same cell and is connected vertically to the selected
                # tile, check that no horizontal cell connections "block" the vertical tile connection.
                # If indeed no cell connections block the tile connection, add the adjacent tile to the cycle.
                elif adj_conn in ['u', 'd']:
                    if not (('l' in cell_conn and cell_pos[0] == 0) or ('r' in cell_conn and cell_pos[0] == 1)):
                        cycle.append(adj_tile)
                        break
                # Otherwise, repeat for horizontal tile connections.
                elif not (('u' in cell_conn and cell_pos[1] == 0) or ('d' in cell_conn and cell_pos[1] == 1)):
                    cycle.append(adj_tile)
                    break

    # If the snake is facing the opposite direction from the cycle, flip the cycle's direction.
    if cycle.index(snake[1]) == 1:
        cycle = cycle[::-1]
    print(cycle)
    return cycle


# The is_ordered function takes in the current Hamiltonian Cycle and a snake's body segments, and returns whether or not
# the snake is ordered (body is after the tail and before the head) within the cycle.
# EXAMPLES:
# EMPTY-TAIL-BODY-HEAD-EMPTY    > ORDERED
# BODY-HEAD-EMPTY-TAIL-BODY     > ORDERED
# EMPTY-HEAD-BODY-TAIL-EMPTY    > NOT ORDERED
# EMPTY-BODY-TAIL-HEAD-EMPTY    > NOT ORDERED
def is_ordered(cycle, segments):
    head = segments[0]
    tail = segments[-1]
    head_index = cycle.index(head)
    tail_index = cycle.index(tail)

    # If the head has overtaken the tail in the cycle, check that no snake segments appear before the tail or after
    # the head.
    if head_index > tail_index:
        for i in range(0, tail_index):
            if cycle[i] in segments:
                return False
        for i in range(head_index + 1, len(cycle)):
            if cycle[i] in segments:
                return False
    # If the tail has overtaken the head, check that no snake segments appear between the head and the tail.
    else:
        for i in range(head_index + 1, tail_index):
            if cycle[i] in segments:
                return False
    return True


# The generate_move function takes in the current Snake object, the current food position and the Hamiltonian Cycle and
# finds the next optimal move for the snake.
def generate_move(snake, food_pos, cycle):
    if not food_pos:  # If there is no food generated, act as though there is food at (0, 0) in order to avoid errors.
        food_pos = (0, 0)
    head_pos = snake[0]
    food_index = cycle.index(food_pos)
    head_index = cycle.index(head_pos)

    # The dir_dict dictionary contains information about the tiles bordering the snakes head, and their relative
    # direction to it.
    dir_dict = get_dir_dict(head_pos[0], head_pos[1], w - 1, h - 1)

    # Sets the next position the snake will move to as the next position in the Hamiltonian Cycle. Default case in the
    # situation that no better shortcut is found for the snake to take.
    if head_index < len(cycle) - 1:
        next_pos = cycle[head_index + 1]
    else:
        next_pos = cycle[0]

    # Edge case, in case the snake has grown rapidly and the next position in the Hamiltonian Cycle will result in the
    # snake crashing into itself, select the first available tile to move to.
    if next_pos in snake:
        for adj in dir_dict.keys():
            if adj not in snake:
                next_pos = adj
                break

    # Default case, set the best_skip (the best move for the snake to take) as the next position in the Hamiltonian
    # Cycle, paired with it's distance to the food.
    next_pos_dist = food_index - cycle.index(next_pos)
    best_skip = (next_pos, next_pos_dist)

    # Only check for shortcuts if the snake takes up less than 85% of the game grid.
    if len(snake) < (w * h) * 0.85:
        # Repeat for all adjacent tiles "skips" that are not a part of the snake's body:
        for skip in dir_dict.keys():
            if skip not in snake:
                # Check if the snake's body will be ordered if the skip is taken.
                new_segments = [skip] + snake
                if is_ordered(cycle, new_segments):
                    # Calculate the distance to the food if the skip is taken.
                    skip_dist = food_index - cycle.index(skip)
                    if skip_dist < 0:
                        skip_dist = len(cycle) - abs(skip_dist)

                    # If the skip is better than the current best skip, set the skip as the new best skip.
                    if skip_dist < best_skip[1]:
                        best_skip = (skip, skip_dist)
    return dir_dict[best_skip[0]]


if __name__ == '__main__':
    game = SnakeGame()

    while True:

        game_over, score = game.play_step()

        if game_over:
            game.endScreen()

    print('Final score:', score)

    pygame.quit()
