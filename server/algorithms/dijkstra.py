import heapq


def dijkstras(grid, start_node):
    directions = [
        {"row": -1, "col": 0},
        {"row": 0, "col": 1},
        {"row": 1, "col": 0},
        {"row": 0, "col": -1},
    ]
    count = 0
    distance = {}
    min_heap = []
    visited_nodes = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not grid[i][j]["isStart"] and not grid[i][j]["isWall"]:
                distance[(i, j)] = float("inf")
                heapq.heappush(min_heap, (distance[(i, j)], count, (i, j)))
    distance[(start_node["row"], start_node["col"])] = 0
    heapq.heappush(
        min_heap,
        (
            distance[(start_node["row"], start_node["col"])],
            count,
            (start_node["row"], start_node["col"]),
        ),
    )
    while (
        len(min_heap) != 0
        and not grid[min_heap[0][2][0]][min_heap[0][2][1]]["isFinish"]
    ):
        current = heapq.heappop(min_heap)
        current_distance = current[0]
        (current_row, current_col) = current[2]
        current_location = {"row": current_row, "col": current_col}
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
                neighbor_distance = current_distance + neighbor["distance"]
                if (
                    not neighbor["isWall"]
                    and neighbor_distance < distance[(neighbor_row, neighbor_col)]
                ):
                    distance[(neighbor_row, neighbor_col)] = neighbor_distance
                    neighbor["previousNode"] = current_location
                    count += 1
                    heapq.heappush(
                        min_heap,
                        (neighbor_distance, count, (neighbor_row, neighbor_col)),
                    )
        visited_nodes.append(grid[current_row][current_col])
    if len(min_heap) != 0:
        visited_nodes.append(grid[min_heap[0][2][0]][min_heap[0][2][1]])
    return visited_nodes, grid
