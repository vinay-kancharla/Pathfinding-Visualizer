def breadth_first_search(grid, start_node):
    directions = [
        {"row": -1, "col": 0},
        {"row": 0, "col": 1},
        {"row": 1, "col": 0},
        {"row": 0, "col": -1},
    ]
    queue = [start_node]
    visited = {f'{start_node["row"]}-{start_node["col"]}'}
    visited_nodes = []
    current = None
    while len(queue) != 0 and queue[0]["isFinish"] is False:
        current = queue.pop(0)
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
                    queue.append(neighbor)
                    visited.add(neighbor_location)
        visited_nodes.append(current)
    if len(queue) != 0:
        visited_nodes.append(queue[0])
    return visited_nodes, grid
