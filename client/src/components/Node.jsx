function Node({
	row,
	col,
	isFinish,
	isStart,
	distance,
	initialDistance,
	isWall,
	isVisited,
	isPath,
	onMouseDown,
	onMouseEnter,
	onMouseUp,
}) {
	const extraClassName = isPath
		? "node-path"
		: isFinish
		? "node-finish"
		: isStart
		? "node-start"
		: isVisited
		? "node-visited"
		: isWall
		? "node-wall"
		: "";

	return (
		<div
			id={`node-${row}-${col}`}
			className={`node ${extraClassName}`}
			onMouseDown={() => onMouseDown(row, col)}
			onMouseEnter={() => onMouseEnter(row, col)}
			onMouseUp={() => onMouseUp()}
			draggable={isStart || isFinish}
			style={{ color: isStart ? "green" : isFinish ? "red" : "" }}
		>
			{isStart
				? "S"
				: isFinish
				? "F"
				: distance !== initialDistance && distance}
		</div>
	);
}

export default Node;
