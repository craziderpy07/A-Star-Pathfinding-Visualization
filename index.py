import pygame
import heapq
import random

pygame.init()

# Configs
WIDTH = 600
ROWS = 30
INFO_HEIGHT = 140
WIN = pygame.display.set_mode((WIDTH, WIDTH + INFO_HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

FONT = pygame.font.SysFont("arial", 18)
SMALL_FONT = pygame.font.SysFont("arial", 14)

SPEEDS = {1: 60, 2: 20, 3: 0}
current_speed = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (220, 220, 220)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)
ORANGE = (255, 165, 0)
PURPLE = (140, 0, 140)
HOVER = (180, 180, 255)
BUTTON = (240, 240, 240)
BUTTON_HOVER = (200, 200, 200)
BUTTON_ACTIVE = (100, 180, 255)

# Prevent user from doing anything else after A* is ran
astar_ran = False


# Button
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.active = False

    def draw(self, win):
        mouse = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse) else BUTTON
        if self.active:
            color = BUTTON_ACTIVE
        pygame.draw.rect(win, color, self.rect, border_radius=6)
        pygame.draw.rect(win, BLACK, self.rect, 2, border_radius=6)

        txt = FONT.render(self.text, True, BLACK)
        win.blit(
            txt,
            (self.rect.centerx - txt.get_width() // 2,
             self.rect.centery - txt.get_height() // 2)
        )

    def click(self):
        self.action()


# User's Start and End dots on the grid
class Spot:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.size = size
        self.color = WHITE
        self.neighbors = []

    def is_wall(self):
        return self.color == BLACK

    def draw(self, win, hover=False):
        color = HOVER if hover and self.color == WHITE else self.color
        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size))

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


def reconstruct_path(came_from, current, start, draw_fn):
    """
    Colors the final path (excluding start/end) and returns the number of BLUE tiles drawn.
    draw_fn is expected to be a function like: draw_fn(explored, open_size)
    """
    steps = 0
    while current in came_from:
        current = came_from[current]
        if current == start:
            break
        current.color = BLUE
        steps += 1
        draw_fn(0, None)  # <-- FIX: positional args to match your lambda
        pygame.time.delay(SPEEDS[current_speed])
    return steps


def a_star(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}

    g = {spot: float("inf") for row in grid for spot in row}
    g[start] = 0
    f = {spot: float("inf") for row in grid for spot in row}
    f[start] = heuristic((start.row, start.col), (end.row, end.col))

    open_hash = {start}
    explored = 0
    last_open_size = len(open_hash)

    while open_set:
        pygame.event.pump()
        last_open_size = len(open_hash)

        current = heapq.heappop(open_set)[2]
        open_hash.remove(current)
        explored += 1

        if current == end:
            steps = reconstruct_path(came_from, end, start, draw)
            return g[end], steps, explored, True, last_open_size

        for neighbor in current.neighbors:
            temp = g[current] + 1
            if temp < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp
                f[neighbor] = temp + heuristic(
                    (neighbor.row, neighbor.col),
                    (end.row, end.col)
                )

                if neighbor not in open_hash:
                    count += 1
                    heapq.heappush(open_set, (f[neighbor], count, neighbor))
                    open_hash.add(neighbor)
                    neighbor.color = GREEN

        draw(explored, len(open_hash))
        if current != start:
            current.color = RED

        pygame.time.delay(SPEEDS[current_speed])

    return None, None, explored, False, last_open_size


# Grid
def make_grid():
    size = WIDTH // ROWS
    return [[Spot(i, j, size) for j in range(ROWS)] for i in range(ROWS)]


def draw_grid():
    gap = WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(WIN, GREY, (0, i * gap), (WIDTH, i * gap))
        pygame.draw.line(WIN, GREY, (i * gap, 0), (i * gap, WIDTH))


# User Interface
final_open_size = 0


def draw_info(explored, open_size, cost, steps, status):
    pygame.draw.rect(WIN, GREY, (0, WIDTH, WIDTH, INFO_HEIGHT))

    if not start:
        msg = "Step 1: Click to place a START point."
    elif not end:
        msg = "Step 2: Click to place an END point."
    else:
        msg = "Step 3: Right-click to Generate Walls. Set a speed and Run A*."

    WIN.blit(FONT.render(msg, True, RED), (10, WIDTH + 5))

    size_to_display = open_size if open_size is not None else final_open_size
    stats = f"Explored: {explored} | Open Set: {size_to_display} | Speed: {current_speed}x"
    WIN.blit(SMALL_FONT.render(stats, True, BLACK), (10, WIDTH + 30))

    if status:
        WIN.blit(SMALL_FONT.render(status, True, RED), (10, WIDTH + 50))
    elif cost is not None:
        WIN.blit(SMALL_FONT.render(f"Cost: {cost} | Steps: {steps}", True, BLACK),
                 (10, WIDTH + 50))

    for btn in buttons:
        btn.draw(WIN)


def draw(explored=0, open_size=None, cost=None, steps=None, status=""):
    WIN.fill(WHITE)
    mx, my = pygame.mouse.get_pos()
    gap = WIDTH // ROWS

    for row in grid:
        for spot in row:
            hover = (spot.row == my // gap and spot.col == mx // gap and my < WIDTH)
            spot.draw(WIN, hover)

    draw_grid()
    draw_info(explored, open_size, cost, steps, status)
    pygame.display.update()


# Actions
def run_astar():
    global cost, steps, explored, status, final_open_size, astar_ran
    if not start or not end:
        status = "Place START and END first!"
        return

    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    cost, steps, explored, success, final_open_size = a_star(
        lambda e, o: draw(e, o, cost, steps, status),
        grid, start, end
    )
    status = "" if success else "No possible path was found!"

    # Locks the grid after running A*
    astar_ran = True


def reset_grid():
    global grid, start, end, cost, steps, explored, status, final_open_size, astar_ran
    grid = make_grid()
    start = end = None
    cost = steps = explored = 0
    final_open_size = 0
    status = ""

    # Unlocks the grid
    astar_ran = False


def clear_walls():
    # Locks the wall clearing after A* is ran
    if astar_ran:
        return
    for row in grid:
        for spot in row:
            if spot.color == BLACK:
                spot.color = WHITE


def set_speed(speed):
    global current_speed
    current_speed = speed
    for btn in buttons:
        btn.active = btn.text.startswith(str(speed))


def random_walls(density=0.25):
    # Locks the random walls after A* is ran
    if astar_ran:
        return
    for row in grid:
        for spot in row:
            if spot not in (start, end):
                spot.color = BLACK if random.random() < density else WHITE


grid = make_grid()
start = end = None
cost = steps = explored = 0
status = ""
final_open_size = 0

button_y = WIDTH + 95
buttons = [
    Button(10, button_y, 120, 32, "Run A*", run_astar),
    Button(140, button_y, 120, 32, "Reset", reset_grid),
    Button(270, button_y, 150, 32, "Clear Walls", clear_walls),
    Button(450, button_y, 40, 32, "1x", lambda: set_speed(1)),
    Button(500, button_y, 40, 32, "2x", lambda: set_speed(2)),
    Button(550, button_y, 40, 32, "3x", lambda: set_speed(3)),
    Button(270, button_y - 40, 150, 32, "Generate Walls", lambda: random_walls(0.25))
]

set_speed(current_speed)


def main():
    global start, end

    run = True
    while run:
        draw(explored, None, cost, steps, status)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn.rect.collidepoint(event.pos):
                        btn.click()
                        break

            mx, my = pygame.mouse.get_pos()
            # Prevents the user from editing the grid after A* is ran
            if my >= WIDTH or astar_ran:
                continue

            row = my * ROWS // WIDTH
            col = mx * ROWS // WIDTH
            if not (0 <= row < ROWS and 0 <= col < ROWS):
                continue

            spot = grid[row][col]

            if pygame.mouse.get_pressed()[0]:
                if not start and not spot.is_wall():
                    start = spot
                    spot.color = ORANGE
                elif not end and not spot.is_wall():
                    end = spot
                    spot.color = PURPLE

            if pygame.mouse.get_pressed()[2]:
                if spot not in (start, end):
                    spot.color = BLACK

    pygame.quit()

main()
