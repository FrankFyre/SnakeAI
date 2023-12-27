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

BLOCK_SIZE = 30

winW = 600
winH = 600
max_len = (winW // BLOCK_SIZE) * (winH // BLOCK_SIZE)

font = pygame.font.SysFont('arial', 25)

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
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0

        self.food = Point(x=0, y=0)
        self.padLR = 0  # 20
        self.padT = 0  # 40
        self.padB = 0  # 20
        self.complete = False
        self.speed = 20
        self.placeholder = 0


    # creates the food
    def place_food(self):
        '''
        x = random.randint(20, self.w - (self.padLR * 2)) // BLOCK_SIZE * BLOCK_SIZE
        y = random.randint(0, self.h - (self.padT + self.padB)) // BLOCK_SIZE * BLOCK_SIZE
        '''

        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE



        if not self.complete:
        #tryign to fix food spawn in same place even though snake occupied
            self.food = Point(x+BLOCK_SIZE, y)

        # Ensure food is not in snake occupied path

            if self.food in self.snake:
                self.place_food()

    def check_completion(self):
        if len(self.snake) == max_len:
            self.complete = True

        else:
            self.complete = False

    def _is_collision(self):
        # hit the wall

        if self.head.x > self.w + BLOCK_SIZE \
                or self.head.x < BLOCK_SIZE \
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

    def change_direction(self, direction):
        if direction == 'up' and self.direction != 'down':
            self.direction = Direction.UP

        if direction == 'down' and self.direction != 'up':
            self.direction = Direction.DOWN

        if direction == 'right' and self.direction != 'left':
            self.direction = Direction.LEFT

        if direction == 'left' and self.direction != 'right':
            self.direction = Direction.RIGHT


    def endScreen(self):
        # Sets a translucent gray overlay on top of the game window.
        trans = pygame.Surface((self.w, self.h))
        trans.set_alpha(210)
        trans.fill(BLACK)
        self.display.blit(trans, (0, 0))



        # Displays the "GAME OVER" text.
        text = font.render("GAME WON", True, WHITE)
        text_rect = text.get_rect(center=(self.w // 2, self.h // 2 - BLOCK_SIZE // 2))
        text2 = font.render("Score:" + str(self.score), True, WHITE)
        text_rect2 = text2.get_rect(center=(self.w // 2, (self.h // 2 - BLOCK_SIZE // 2)+BLOCK_SIZE))
        self.display.blit(text, text_rect)
        self.display.blit(text2, text_rect2)
        pygame.display.flip()

    def _update_ui(self):
        self.display.fill(BLACK)


        r = 255
        g = 216
        b = 0
        gradient = 0

        for i, pt in enumerate(self.snake):
            finalcolor = (r, max(g - gradient, 0), b)  # Ensure finalG does not go below 0

            # if i == 0:  # Head of the snake
            #     pygame.draw.rect(self.display, finalcolor,
            #                      pygame.Rect(pt.x - BLOCK_SIZE, pt.y, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
            # else:
            #     # For the body segments
            pygame.draw.rect(self.display, finalcolor,
                             pygame.Rect(pt.x - BLOCK_SIZE, pt.y, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
            spread = len(self.snake)
            gradient += (g / spread)

        # food
        if not self.complete:
            pygame.draw.rect(self.display, BLUE,
                             pygame.Rect(self.food.x - BLOCK_SIZE, self.food.y, BLOCK_SIZE-1, BLOCK_SIZE-1))

            text = font.render("Score: " + str(self.score), True, WHITE)
            text_rect = text.get_rect(center=((self.w // 2)//2, 20))
            temp_surface = pygame.Surface(text.get_size())
            pygame.draw.rect(temp_surface, BLACK, (0, 0, *text_rect.size), border_radius=10)
            temp_surface.set_alpha(200)
            temp_surface.fill(BLACK)
            temp_surface.blit(text, (0,0))
            self.display.blit(temp_surface, text_rect)

            text = font.render("Speed: " + str(self.speed/20), True, WHITE)
            text_rect = text.get_rect(center=(((self.w // 2) // 2)+(self.w // 2), 20))
            temp_surface = pygame.Surface(text.get_size())
            pygame.draw.rect(temp_surface, BLACK, (0, 0, *text_rect.size), border_radius=10)
            temp_surface.set_alpha(200)
            temp_surface.fill(BLACK)
            temp_surface.blit(text, (0, 0))
            self.display.blit(temp_surface, text_rect)

        if self.complete:
            self.endScreen()

        pygame.display.flip()

    def play_step(self, cycle):
        # user input


        run = False
        # Check if game is done
        game_over = False
        position = (int(self.head.x / BLOCK_SIZE), int(self.head.y / BLOCK_SIZE))
        # Identifies the position in the hamiltonian cycle at which the snake begins
        index = cycle.index(position)
        length = len(cycle)

        self.place_food()

        # Loop simulates the movement of the snake and controls game mechanics
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    run = True

        while run:
            self.clock.tick(self.speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.speed += 20
                        print(self.speed)
                    elif event.key == pygame.K_DOWN:
                        if self.speed != 20:
                            self.speed -= 20
                            print(self.speed)


            # Finds the direction for the snake's next movement according to the calculated hamiltonian cycle
            if index + 1 < length and cycle[index + 1] == (position[0] + 1, position[1]):
                self.change_direction('right')
                position = (position[0] + 1, position[1])

            elif index + 1 < length and cycle[index + 1] == (position[0] - 1, position[1]):
                self.change_direction('left')
                position = (position[0] - 1, position[1])

            elif index + 1 < length and cycle[index + 1] == (position[0], position[1] + 1):
                self.change_direction('down')
                position = (position[0], position[1] + 1)

            elif index + 1 < length and cycle[index + 1] == (position[0], position[1] - 1):
                self.change_direction('up')
                position = (position[0], position[1] - 1)


            # Takes care of boundary case where the next index of the cycle does not exist
            # The next position is 1st index of the cycle
            # Otherwise the index is incremented by 1
            if index == length - 1:
                if cycle[0] == (position[0] + 1, position[1]):
                    self.change_direction('right')
                    position = (position[0] + 1, position[1])
                elif cycle[0] == (position[0] - 1, position[1]):
                    self.change_direction('left')
                    position = (position[0] - 1, position[1])
                elif cycle[0] == (position[0], position[1] + 1):
                    self.change_direction('down')
                    position = (position[0], position[1] + 1)
                elif cycle[0] == (position[0], position[1] - 1):
                    self.change_direction('up')
                    position = (position[0], position[1] - 1)
                index = 0
            else:
                index += 1



            # Changes the coordinates of the snake's position
            self._move(self.direction)
            self.snake.insert(0, self.head)


            #Not needed as its following maze, disable for the nice moving snake background
            # if self._is_collision():
            #     game_over = True
            #     return game_over, self.score

            # food stuff
            self.check_completion()
            if not self.complete:
                if self.head == self.food:

                    self.score += 1
                    self.place_food()

                else:
                    self.snake.pop()
            else:
                self.snake.pop()

            self._update_ui()

        return game_over, self.score






# Uses prim's algorithm to generate a randomized maze using randomized edge weights
def prim_maze_generator(grid_rows, grid_columns):
    directions = dict()
    vertices = grid_rows * grid_columns

    # Creates keys for the directions dictionary
    # Note that the maze has half the width and length of the grid for the hamiltonian cycle
    for i in range(grid_rows):
        for j in range(grid_columns):
            directions[j, i] = []

    # The initial cell for maze generation is chosen randomly
    x = random.randint(0, grid_columns - 1)
    y = random.randint(0, grid_rows - 1)
    initial_cell = (x, y)

    current_cell = initial_cell

    # Stores all cells that have been visited
    visited = [initial_cell]

    # Contains all neighbouring cells to cells that have been visited
    adj_cells = set()

    # Generates walls in grid randomly to create a randomized maze
    while len(visited) != vertices:

        # Stores the position of the current cell in the grid
        x_position = current_cell[0]
        y_position = current_cell[1]

        # Finds adjacent cells when the current cell does not lie on the edge of the grid
        if x_position != 0 and y_position != 0 and x_position != grid_columns - 1 and y_position != grid_rows - 1:
            adj_cells.add((x_position, y_position - 1))
            adj_cells.add((x_position, y_position + 1))
            adj_cells.add((x_position - 1, y_position))
            adj_cells.add((x_position + 1, y_position))

        # Finds adjacent cells when the current cell lies in the left top corner of the grid
        elif x_position == 0 and y_position == 0:
            adj_cells.add((x_position + 1, y_position))
            adj_cells.add((x_position, y_position + 1))

        # Finds adjacent cells when the current cell lies in the bottom left corner of the grid
        elif x_position == 0 and y_position == grid_rows - 1:
            adj_cells.add((x_position, y_position - 1))
            adj_cells.add((x_position + 1, y_position))

        # Finds adjacent cells when the current cell lies in the left column of the grid
        elif x_position == 0:
            adj_cells.add((x_position, y_position - 1))
            adj_cells.add((x_position, y_position + 1))
            adj_cells.add((x_position + 1, y_position))

        # Finds adjacent cells when the current cell lies in the top right corner of the grid
        elif x_position == grid_columns - 1 and y_position == 0:
            adj_cells.add((x_position, y_position + 1))
            adj_cells.add((x_position - 1, y_position))

        # Finds adjacent cells when the current cell lies in the bottom right corner of the grid
        elif x_position == grid_columns - 1 and y_position == grid_rows - 1:
            adj_cells.add((x_position, y_position - 1))
            adj_cells.add((x_position - 1, y_position))

        # Finds adjacent cells when the current cell lies in the right column of the grid
        elif x_position == grid_columns - 1:
            adj_cells.add((x_position, y_position - 1))
            adj_cells.add((x_position, y_position + 1))
            adj_cells.add((x_position - 1, y_position))

        # Finds adjacent cells when the current cell lies in the top row of the grid
        elif y_position == 0:
            adj_cells.add((x_position, y_position + 1))
            adj_cells.add((x_position - 1, y_position))
            adj_cells.add((x_position + 1, y_position))

        # Finds adjacent cells when the current cell lies in the bottom row of the grid
        else:
            adj_cells.add((x_position, y_position - 1))
            adj_cells.add((x_position + 1, y_position))
            adj_cells.add((x_position - 1, y_position))

        # Generates a wall between two cells in the grid
        while current_cell:

            current_cell = (adj_cells.pop())

            # The neighbouring cell is disregarded if it is already a wall in the maze
            if current_cell not in visited:

                # The neighbouring cell is now classified as having been visited
                visited.append(current_cell)
                x = current_cell[0]
                y = current_cell[1]

                # To generate a wall, a cell adjacent to the current cell must already have been visited
                # The direction of the wall between cells is stored
                # The process is simplified by only considering a wall to be to the right or down
                if (x + 1, y) in visited:
                    directions[x, y] += ['right']
                elif (x - 1, y) in visited:
                    directions[x - 1, y] += ['right']
                elif (x, y + 1) in visited:
                    directions[x, y] += ['down']
                elif (x, y - 1) in visited:
                    directions[x, y - 1] += ['down']

                break

    # Provides the hamiltonian cycle generating algorithm with the direction of the walls to avoid
    return hamiltonian_cycle(grid_rows, grid_columns, directions)


# Finds a hamiltonian cycle for the snake to follow to prevent collisions with its body segments
def hamiltonian_cycle(grid_rows, grid_columns, orientation):
    # The path for the snake is stored in a dictionary
    # The keys are the (x, y) positions in the grid
    # The values are the adjacent (x, y) positions that the snake can travel towards
    hami_graph = dict()

    # Uses the coordinates of the walls to generate available adjacent cells for each cell
    # Simplified by only considering the right and down directions
    for i in range(grid_rows):
        for j in range(grid_columns):

            # Finds available adjacent cells if current cell does not lie on an edge of the grid
            if j != grid_columns - 1 and i != grid_rows - 1 and j != 0 and i != 0:
                if 'right' in orientation[j, i]:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                    hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                else:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' in orientation[j, i]:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                    if (j * 2 + 1, i * 2 + 1) in hami_graph:
                        hami_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                else:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' not in orientation[j, i - 1]:
                    hami_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                if 'right' not in orientation[j - 1, i]:
                    if (j * 2, i * 2) in hami_graph:
                        hami_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                    else:
                        hami_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

            # Finds available adjacent cells if current cell is in the bottom right corner
            elif j == grid_columns - 1 and i == grid_rows - 1:
                hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' not in orientation[j, i - 1]:
                    hami_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                elif 'right' not in orientation[j - 1, i]:
                    hami_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

            # Finds available adjacent cells if current cell is in the top right corner
            elif j == grid_columns - 1 and i == 0:
                hami_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' in orientation[j, i]:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                    hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                else:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                if 'right' not in orientation[j - 1, i]:
                    hami_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]

            # Finds available adjacent cells if current cell is in the right column
            elif j == grid_columns - 1:
                hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' in orientation[j, i]:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                    hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                else:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' not in orientation[j, i - 1]:
                    hami_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                if 'right' not in orientation[j - 1, i]:
                    if (j * 2, i * 2) in hami_graph:
                        hami_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                    else:
                        hami_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

            # Finds available adjacent cells if current cell is in the top left corner
            elif j == 0 and i == 0:
                hami_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                hami_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                if 'right' in orientation[j, i]:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                    hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                else:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' in orientation[j, i]:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                    if (j * 2 + 1, i * 2 + 1) in hami_graph:
                        hami_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                else:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]

            # Finds available adjacent cells if current cell is in the bottom left corner
            elif j == 0 and i == grid_rows - 1:
                hami_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]
                hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                if 'right' in orientation[j, i]:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                    hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                else:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' not in orientation[j, i - 1]:
                    hami_graph[j * 2, i * 2] += [(j * 2 + 1, i * 2)]

            # Finds available adjacent cells if current cell is in the left corner
            elif j == 0:
                hami_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]
                if 'right' in orientation[j, i]:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                    hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                else:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' in orientation[j, i]:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                    if (j * 2 + 1, i * 2 + 1) in hami_graph:
                        hami_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                else:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' not in orientation[j, i - 1]:
                    hami_graph[j * 2, i * 2] += [(j * 2 + 1, i * 2)]

            # Finds available adjacent cells if current cell is in the top row
            elif i == 0:
                hami_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                if 'right' in orientation[j, i]:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                    hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                else:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' in orientation[j, i]:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                    if (j * 2 + 1, i * 2 + 1) in hami_graph:
                        hami_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                else:
                    hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                if 'right' not in orientation[j - 1, i]:
                    hami_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]

            # Finds available adjacent cells if current cell is in the bottom row
            else:
                hami_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                if 'right' in orientation[j, i]:
                    hami_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                else:
                    hami_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                if 'down' not in orientation[j, i - 1]:
                    hami_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                if 'right' not in orientation[j - 1, i]:
                    if (j * 2, i * 2) in hami_graph:
                        hami_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                    else:
                        hami_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

    # Provides the coordinates of available adjacent cells to generate directions for the snake's movement
    return path_generator(hami_graph, grid_rows * grid_columns * 4)


# Generates a path composed of coordinates for the snake to travel along
def path_generator(graph, cells):
    # The starting position for the path is at cell (0, 0)
    starting_point = (0, 0)
    path = [starting_point]

    previous_cell = path[0]
    previous_direction = None

    # Generates a path that is a hamiltonian cycle by following a set of general laws
    # 1. If the right cell is available, travel to the right
    # 2. If the cell underneath is available, travel down
    # 3. If the left cell is available, travel left
    # 4. If the cell above is available, travel up
    # 5. The current direction cannot oppose the previous direction (e.g. left --> right)
    while len(path) != cells:
        if previous_cell in graph and (previous_cell[0] + 1, previous_cell[1]) in graph[previous_cell] \
                and previous_direction != 'left':
            path.append((previous_cell[0] + 1, previous_cell[1]))
            previous_cell = (previous_cell[0] + 1, previous_cell[1])
            previous_direction = 'right'
        elif previous_cell in graph and (previous_cell[0], previous_cell[1] + 1) in graph[previous_cell] \
                and previous_direction != 'up':
            path.append((previous_cell[0], previous_cell[1] + 1))
            previous_cell = (previous_cell[0], previous_cell[1] + 1)
            previous_direction = 'down'
        elif (previous_cell[0] - 1, previous_cell[1]) in graph \
                and previous_cell in graph[previous_cell[0] - 1, previous_cell[1]] and previous_direction != 'right':
            path.append((previous_cell[0] - 1, previous_cell[1]))
            previous_cell = (previous_cell[0] - 1, previous_cell[1])
            previous_direction = 'left'
        else:
            path.append((previous_cell[0], previous_cell[1] - 1))
            previous_cell = (previous_cell[0], previous_cell[1] - 1)
            previous_direction = 'up'

    return path


if __name__ == '__main__':
    game = SnakeGame()
    #width has to eb 2 times the block size
    circuit = prim_maze_generator(int(winH / (BLOCK_SIZE * 2)), int(winW / (BLOCK_SIZE * 2)))

    while True:

        game_over, score = game.play_step(circuit)

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
