import heapq


def heuristic(node_location, finish_node_location):
    x1, y1 = node_location
    x2, y2 = finish_node_location
    return abs(x1 - x2) + abs(y1 - y2)


def astar_search(grid, start_node, finish_node):
    directions = [
        {"row": -1, "col": 0},
        {"row": 0, "col": 1},
        {"row": 1, "col": 0},
        {"row": 0, "col": -1},
    ]
    count = 0
    min_heap = []
    visited = {(start_node["row"], start_node["col"])}
    visited_nodes = []
    g_score = {}
    f_score = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not grid[i][j]["isStart"] and not grid[i][j]["isWall"]:
                g_score[(i, j)] = float("inf")
                f_score[(i, j)] = float("inf")
    g_score[(start_node["row"], start_node["col"])] = 0
    f_score[(start_node["row"], start_node["col"])] = heuristic(
        (start_node["row"], start_node["col"]), (finish_node["row"], finish_node["col"])
    )
    heapq.heappush(min_heap, (0, count, (start_node["row"], start_node["col"])))
    while (
        len(min_heap) != 0
        and not grid[min_heap[0][2][0]][min_heap[0][2][1]]["isFinish"]
    ):
        current = heapq.heappop(min_heap)
        (current_row, current_col) = current[2]
        current_location = {"row": current_row, "col": current_col}
        visited.remove((current_row, current_col))
        for direction in directions:
            neighbor_row = current_row + direction["row"]
            neighbor_col = current_col + direction["col"]
            in_bounds = (
                0 <= neighbor_row
                and neighbor_row < len(grid)
                and 0 <= neighbor_col
                and neighbor_col < len(grid[0])
            )
            if in_bounds:
                neighbor = grid[neighbor_row][neighbor_col]
                temp_g_score = (
                    g_score[(current_row, current_col)] + neighbor["distance"]
                )
                if (
                    not neighbor["isWall"]
                    and temp_g_score < g_score[(neighbor_row, neighbor_col)]
                ):
                    neighbor["previousNode"] = current_location
                    g_score[(neighbor_row, neighbor_col)] = temp_g_score
                    f_score[(neighbor_row, neighbor_col)] = temp_g_score + heuristic(
                        (neighbor_row, neighbor_col),
                        (finish_node["row"], finish_node["col"]),
                    )
                    if (neighbor_row, neighbor_col) not in visited:
                        count += 1
                        heapq.heappush(
                            min_heap,
                            (
                                f_score[(neighbor_row, neighbor_col)],
                                count,
                                (neighbor_row, neighbor_col),
                            ),
                        )
                        visited.add((neighbor_row, neighbor_col))
        visited_nodes.append(grid[current_row][current_col])
    if len(min_heap) != 0:
        visited_nodes.append(grid[min_heap[0][2][0]][min_heap[0][2][1]])
    return visited_nodes, grid
