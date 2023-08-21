import random


def generate_maze(grid):
    s = set()
    (row, col) = (
        random.choice(list(range(1, len(grid), 2))),
        random.choice(list(range(1, len(grid[0]), 2))),
    )
    grid[row][col]["isWall"] = False
    fs = get_frontiers(row, col, grid)
    for f in fs:
        s.add(f)
    while s:
        row, col = random.choice(tuple(s))
        s.remove((row, col))
        ns = get_neighbors(row, col, grid)
        if ns:
            n_row, n_col = random.choice(tuple(ns))
            connect(row, col, n_row, n_col, grid)
        fs = get_frontiers(row, col, grid)
        for f in fs:
            s.add(f)
    return grid


def get_frontiers(row, col, grid):
    frontiers = set()
    if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]):
        if row - 2 > 0 and grid[row - 2][col]["isWall"]:
            frontiers.add((row - 2, col))
        if row + 2 < len(grid) - 1 and grid[row + 2][col]["isWall"]:
            frontiers.add((row + 2, col))
        if col - 2 > 0 and grid[row][col - 2]["isWall"]:
            frontiers.add((row, col - 2))
        if col + 2 < len(grid[0]) - 1 and grid[row][col + 2]["isWall"]:
            frontiers.add((row, col + 2))
    return frontiers


def get_neighbors(row, col, grid):
    neighbors = set()
    if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]):
        if row - 2 > 0 and not grid[row - 2][col]["isWall"]:
            neighbors.add((row - 2, col))
        if row + 2 < len(grid) - 1 and not grid[row + 2][col]["isWall"]:
            neighbors.add((row + 2, col))
        if col - 2 > 0 and not grid[row][col - 2]["isWall"]:
            neighbors.add((row, col - 2))
        if col + 2 < len(grid[0]) - 1 and not grid[row][col + 2]["isWall"]:
            neighbors.add((row, col + 2))
    return neighbors


def connect(row1, col1, row2, col2, grid):
    row = (row1 + row2) // 2
    col = (col1 + col2) // 2
    grid[row1][col1]["isWall"] = False
    grid[row][col]["isWall"] = False
