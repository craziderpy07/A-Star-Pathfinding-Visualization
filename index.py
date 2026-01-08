import pygame
import random
import heapq

pygame.init()

# Set the size of the window and board
WIDTH = 600
ROWS = 30
INFO_HEIGHT = 70
WIN = pygame.display.set_mode((WIDTH, WIDTH + INFO_HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

FONT = pygame.font.SysFont("arial", 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

class Spot:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == BLACK

    def make_wall(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def make_path(self):
        self.color = BLUE

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color,
                         (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

# A* Algo
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    steps = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        steps += 1
    return steps

def a_star(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_hash = {start}

    while open_set:
        pygame.event.pump()
        current = heapq.heappop(open_set)[2]
        open_hash.remove(current)

        if current == end:
            steps = reconstruct_path(came_from, end)
            return g_score[end], steps, True

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(
                    neighbor.get_pos(), end.get_pos())

                if neighbor not in open_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    # If no path is found
    return None, None, False

# Grid board
def make_grid():
    grid = []
    gap = WIDTH // ROWS
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            spot = Spot(i, j, gap)
            if random.random() < 0.25:
                spot.make_wall()
            grid[i].append(spot)
    return grid

def draw_grid():
    gap = WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(WIN, GREY, (0, i * gap), (WIDTH, i * gap))
        pygame.draw.line(WIN, GREY, (i * gap, 0), (i * gap, WIDTH))

def draw(grid, cost=None, steps=None, status=""):
    WIN.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(WIN)

    draw_grid()

    # Controls
    controls = "Left-click: Start/End | Space: Run | R: Reset"
    WIN.blit(FONT.render(controls, True, BLACK), (10, WIDTH + 5))

    if status:
        WIN.blit(FONT.render(status, True, RED), (10, WIDTH + 30))
    elif cost is not None:
        
        # Displays the path cost alongside the steps
        stats = f"Optimal Path Cost: {cost}   Steps: {steps}"
        WIN.blit(FONT.render(stats, True, BLACK), (10, WIDTH + 30))

    pygame.display.update()

def get_pos(pos):
    gap = WIDTH // ROWS
    y, x = pos
    return y // gap, x // gap

def main():
    grid = make_grid()
    start = end = None
    cost = steps = None
    status = ""

    run = True
    while run:
        draw(grid, cost, steps, status)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                row, col = get_pos(pygame.mouse.get_pos())
                spot = grid[row][col]

                if not start and not spot.is_wall():
                    start = spot
                    start.make_start()
                elif not end and not spot.is_wall():
                    end = spot
                    end.make_end()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    cost, steps, success = a_star(
                        lambda: draw(grid, cost, steps, status),
                        grid, start, end
                    )
                    # Displays that there are no possible paths found
                    status = "" if success else "No possible paths were found!"

                if event.key == pygame.K_r:
                    start = end = None
                    cost = steps = None
                    status = ""
                    grid = make_grid()

    pygame.quit()

main()
