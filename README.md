# A* Pathfinding Visualization

## Overview

The A* Pathfinding Visualization is an interactive application developed using Python and Pygame that implements the A* search algorithm to identify and visualize the shortest path between two points on a grid containing obstacles. The application enables users to configure starting and destination points, generate obstacles, and adjust visualization speeds. Through real-time visualization, the project demonstrates heuristic-based search, node exploration, and shortest-path determination.  

<img width="602" height="772" alt="image" src="https://github.com/user-attachments/assets/9370700e-4365-474a-906c-d5a7016abd30" />

## Features

- **Interactive Grid:** Configure starting and destination points within a 30 × 30 grid.
- **A* Search Algorithm:** Determine the shortest available path while avoiding obstacles.
- **Obstacle Configuration:** Manually place obstacles or generate randomized grid environments.
- **Adjustable Visualization Speed:** Control algorithm execution using three speed settings (1x, 2x, and 3x).
- **Real-Time Visualization:** Observe node exploration, path evaluation, and shortest-path reconstruction.
- **Performance Metrics:** Monitor explored nodes, open set size, path cost, and traversal steps.
- **Grid Management:** Reset the grid or remove obstacles to evaluate alternative scenarios.

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application development and algorithm implementation |
| Pygame | Graphical interface and interactive visualization |
| heapq | Priority queue management for node evaluation |
| random | Randomized obstacle generation |

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/craziderpy07/A-Star-Pathfinding-Visualization.git
cd A-Star-Pathfinding-Visualization
```

### 2. Install Dependencies

Ensure Python 3 and pip are installed, then execute:

```bash
pip install pygame
```

### 3. Run the Application

```bash
python index.py
```

## Usage

1. **Set Start and Destination:** Left-click grid cells to define the starting and destination points.
2. **Configure Obstacles:** Right-click to place walls or use "Generate Walls" to create randomized obstacles.
3. **Adjust Speed:** Select 1x, 2x, or 3x to modify visualization speed.
4. **Execute A*:** Select "Run A*" to initiate the pathfinding algorithm.
5. **Observe Results:** View the explored nodes and reconstructed shortest path.
6. **Reset:** Select "Reset" to initialize a new scenario.

## A* Search Algorithm

The A* search algorithm determines the shortest path by combining the accumulated traversal cost with a heuristic estimate of the remaining distance to the destination.

The algorithm evaluates nodes using:

**f(n) = g(n) + h(n)**

Where:

- **g(n):** Actual traversal cost from the starting node.
- **h(n):** Estimated remaining cost to the destination.
- **f(n):** Estimated total path cost.

The application uses the **Manhattan Distance heuristic**, which calculates the horizontal and vertical distance between two grid positions:

```python
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

This heuristic supports efficient pathfinding in grid environments where movement is restricted to four directions.

## Project Structure

```text
A-Star-Pathfinding-Visualization/
├── index.py        # Application and A* algorithm
└── README.md       # Project documentation
```

## Learning Objectives

- Implement heuristic-based pathfinding using the A* search algorithm.
- Apply priority queues and Manhattan Distance for node evaluation.
- Visualize graph traversal and shortest-path reconstruction.
- Examine how obstacles influence pathfinding performance.
- Develop interactive graphical applications using Python and Pygame.
