from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithms.bfs import breadth_first_search
from algorithms.dfs import depth_first_search
from algorithms.dijkstra import dijkstras
from algorithms.astar import astar_search
from algorithms.maze import generate_maze

app = Flask(__name__)
CORS(app)


def handle_traversal(traversal_function):
    data = request.json
    if traversal_function == astar_search:
        visited_nodes, grid = traversal_function(
            data["grid"], data["startNode"], data["finishNode"]
        )
    else:
        visited_nodes, grid = traversal_function(data["grid"], data["startNode"])
    path = []
    if visited_nodes[-1]["isFinish"] is True:
        path = getPath(grid, visited_nodes[-1])
    return jsonify({"visitedNodes": visited_nodes, "path": path})


def getPath(grid, finish_node):
    path = []
    current = {
        "row": finish_node["row"],
        "col": finish_node["col"],
    }
    while current is not None:
        path.append(current)
        current = grid[current["row"]][current["col"]]["previousNode"]
    return path[::-1]


@app.route("/")
def main_page():
    return jsonify("This works!")


@app.route("/bfs", methods={"POST"})
def bfs():
    return handle_traversal(breadth_first_search)


@app.route("/dfs", methods=["POST"])
def dfs():
    return handle_traversal(depth_first_search)


@app.route("/dijkstra", methods=["POST"])
def dijkstra():
    return handle_traversal(dijkstras)


@app.route("/astar", methods=["POST"])
def astar():
    return handle_traversal(astar_search)


@app.route("/maze", methods=["POST"])
def maze():
    data = request.json
    return jsonify({"maze": generate_maze(data["grid"])})


if __name__ == "__main__":
    app.run(debug=True)
