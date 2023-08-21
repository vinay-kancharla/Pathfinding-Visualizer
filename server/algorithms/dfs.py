def depth_first_search(grid, start_node):
    directions = [
        {"row": 0, "col": -1},
        {"row": 1, "col": 0},
        {"row": 0, "col": 1},
        {"row": -1, "col": 0},
    ]
    stack = [start_node]
    visited = set()
    visited_nodes = []
    current = None
    while len(stack) != 0 and stack[-1]["isFinish"] is False:
        current = stack.pop()
        current_location = {"row": current["row"], "col": current["col"]}
        for direction in directions:
            neighbor_row = current["row"] + direction["row"]
            neighbor_col = current["col"] + direction["col"]
            in_bounds = (
                0 <= neighbor_row
                and neighbor_row < len(grid)
                and 0 <= neighbor_col
                and neighbor_col < len(grid[0])
            )
            if in_bounds:
                neighbor = grid[neighbor_row][neighbor_col]
                neighbor_location = f"{neighbor_row}-{neighbor_col}"
                if neighbor_location not in visited and not neighbor["isWall"]:
                    neighbor["previousNode"] = current_location
                    stack.append(neighbor)
        visited_nodes.append(current)
        visited.add(f'{current["row"]}-{current["col"]}')
    if len(stack) != 0:
        visited_nodes.append(stack[-1])
    return visited_nodes, grid
