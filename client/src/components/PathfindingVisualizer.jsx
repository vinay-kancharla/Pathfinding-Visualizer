import Node from "./Node";
import { useState, useEffect } from "react";

const createNode = (row, col, startNode, finishNode) => {
	return {
		row,
		col,
		isStart: row === startNode.row && col === startNode.col,
		isFinish: row === finishNode.row && col === finishNode.col,
		distance: 1,
		isWall: false,
		isVisited: false,
		isPath: false,
		previousNode: null,
	};
};

const createGrid = (startNode, finishNode) => {
	const grid = [];
	for (let row = 0; row < 27; row++) {
		const currentRow = [];
		for (let col = 0; col < 61; col++) {
			currentRow.push(createNode(row, col, startNode, finishNode));
		}
		grid.push(currentRow);
	}
	return grid;
};

const available = (node, mode) => {
	if (mode === "wall") {
		return !node.isStart && !node.isFinish && node.distance === 1;
	} else if (mode === "distance") {
		return !node.isStart && !node.isFinish && !node.isWall;
	}
};

function PathfindingVisualizer() {
	const [grid, setGrid] = useState([]);
	const [startNode, setStartNode] = useState({
		row: 13,
		col: 15,
	});
	const [finishNode, setFinishNode] = useState({
		row: 13,
		col: 45,
	});
	const [mouseIsPressed, setMouseIsPressed] = useState(false);
	const [mode, setMode] = useState();

	useEffect(() => {
		setGrid(createGrid(startNode, finishNode));
	}, [startNode, finishNode]);

	const resetGrid = () => {
		setGrid(createGrid(startNode, finishNode));
	};

	const toggleWall = () => {
		setMode("wall");
	};

	const toggleDistance = () => {
		setMode("distance");
	};

	const clearTraversal = () => {
		const newGrid = grid.map((row) =>
			row.map((node) => ({
				...node,
				isVisited: false,
				isPath: false,
			}))
		);
		setGrid(newGrid);
	};

	const updateGrid = (grid, row, col) => {
		const newGrid = grid.slice();
		const node = newGrid[row][col];
		if (mode === "wall" && available(node, mode)) {
			const newNode = { ...node, isWall: !node.isWall };
			newGrid[row][col] = newNode;
		}
		if (mode === "distance" && available(node, mode)) {
			const newNode = { ...node, distance: ++node.distance };
			newGrid[row][col] = newNode;
		}
		return newGrid;
	};

	const handleMouseDown = (row, col) => {
		const newGrid = updateGrid(grid, row, col);
		setGrid(newGrid);
		setMouseIsPressed(true);
	};

	const handleMouseEnter = (row, col) => {
		if (!mouseIsPressed) return;
		const newGrid = updateGrid(grid, row, col);
		setGrid(newGrid);
		setMouseIsPressed(true);
	};

	const handleMouseUp = () => {
		setMouseIsPressed(false);
	};

	const removeWalls = () => {
		for (let i = 0; i < grid.length; i++) {
			for (let j = 0; j < grid[0].length; j++) {
				if (grid[i][j].isWall) {
					const newGrid = [...grid];
					newGrid[i][j].isWall = false;
					setGrid(newGrid);
				}
			}
		}
	};

	const removeDistances = () => {
		for (let i = 0; i < grid.length; i++) {
			for (let j = 0; j < grid[0].length; j++) {
				if (grid[i][j].distance !== 1) {
					const newGrid = [...grid];
					newGrid[i][j].distance = 1;
					setGrid(newGrid);
				}
			}
		}
	};

	const handleRandomWalls = () => {
		removeWalls();
		for (let i = 0; i < grid.length; i++) {
			for (let j = 0; j < grid[0].length; j++) {
				if (
					available(grid[i][j], "wall") &&
					grid[i][j].distance === 1 &&
					Math.floor(Math.random() * 4) === 0
				) {
					const newGrid = [...grid];
					newGrid[i][j].isWall = true;
					setGrid(newGrid);
				}
			}
		}
	};

	const handleRandomDistances = () => {
		removeDistances();
		for (let i = 0; i < grid.length; i++) {
			for (let j = 0; j < grid[0].length; j++) {
				if (
					available(grid[i][j], "distance") &&
					!grid[i][j].isWall &&
					Math.floor(Math.random() * 2) === 0
				) {
					const newGrid = [...grid];
					newGrid[i][j].distance = Math.floor(Math.random() * 9 + 1);
					setGrid(newGrid);
				}
			}
		}
	};

	const animateMaze = async (maze) => {
		setGrid(maze);
	};

	const animateTraversal = (visitedNodes, path) => {
		for (let i = 0; i <= visitedNodes.length; i++) {
			if (i === visitedNodes.length) {
				setTimeout(() => {
					animatePath(path);
				}, 10 * i);
				return;
			}
			const node = visitedNodes[i];
			setTimeout(() => {
				const newGrid = [...grid];
				newGrid[node.row][node.col].isVisited = false;
				setGrid(newGrid);
			}, 10 * i);
			setTimeout(() => {
				const newGrid = [...grid];
				newGrid[node.row][node.col].isVisited = true;
				setGrid(newGrid);
			}, 10 * i);
		}
	};

	const animatePath = (path) => {
		for (let i = 0; i < path.length; i++) {
			setTimeout(() => {
				const newGrid = [...grid];
				newGrid[path[i].row][path[i].col].isPath = true;
				setGrid(newGrid);
			}, 20 * i);
		}
	};

	const handleTraversal = (traversalName) => async () => {
		clearTraversal();
		try {
			const response = await fetch(`/${traversalName}`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					grid: grid,
					startNode: grid[startNode.row][startNode.col],
					finishNode: grid[finishNode.row][finishNode.col],
				}),
			});
			const data = await response.json();
			animateTraversal(data["visitedNodes"], data["path"]);
		} catch (error) {
			console.log("Error:", error);
		}
	};

	const handleMaze = async () => {
		const newGrid = createGrid(startNode, finishNode);
		for (let i = 0; i < newGrid.length; i++) {
			for (let j = 0; j < newGrid[0].length; j++) {
				newGrid[i][j].isWall = true;
			}
		}
		try {
			const response = await fetch("/maze", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ grid: newGrid }),
			});
			const data = await response.json();
			animateMaze(data["maze"]);
		} catch (error) {
			console.log("Error:", error);
		}
	};

	return (
		<>
			<div className='header-container'>
				<h1>Pathfinding Visualizer</h1>
				<div className='dropdown'>
					<button className='dropdown-button'>Algorithms</button>
					<div className='dropdown-content'>
						<button onClick={handleTraversal("bfs")}>
							Breadth First Search
						</button>

						<button onClick={handleTraversal("dfs")}>
							Depth First Search
						</button>

						<button onClick={handleTraversal("dijkstra")}>
							Dijkstra's
						</button>

						<button onClick={handleTraversal("astar")}>A*</button>
					</div>
				</div>
				<button onClick={resetGrid}>Reset</button>
				<button onClick={clearTraversal}>Clear Traversal</button>
				<button onClick={handleRandomWalls}>Random Walls</button>
				<button onClick={handleRandomDistances}>
					Random Distances
				</button>
				<button onClick={handleMaze}>Generate Maze</button>
				<button onClick={toggleWall}>Toggle Wall</button>
				<button onClick={toggleDistance}>Toggle Distance</button>
			</div>
			<div className='grid-container'>
				{grid.map((row, rowIndex) =>
					row.map((node, colIndex) => (
						<Node
							key={`${rowIndex}-${colIndex}`}
							row={rowIndex}
							col={colIndex}
							isFinish={node.isFinish}
							isStart={node.isStart}
							distance={node.distance}
							initialDistance={1}
							isWall={node.isWall}
							isVisited={node.isVisited}
							isPath={node.isPath}
							mouseIsPressed={mouseIsPressed}
							onMouseDown={() =>
								handleMouseDown(rowIndex, colIndex)
							}
							onMouseEnter={() =>
								handleMouseEnter(rowIndex, colIndex)
							}
							onMouseUp={handleMouseUp}
						/>
					))
				)}
			</div>
		</>
	);
}

export default PathfindingVisualizer;
