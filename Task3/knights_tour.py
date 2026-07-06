from __future__ import annotations
from dataclasses import dataclass, field
__all__ = ["KnightsTourResult", "knights_tour"]

# The eight relative moves a knight can make.
_KNIGHT_MOVES: tuple[tuple[int, int], ...] = (
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1),
)


@dataclass
class KnightsTourResult:
    
    path: list[tuple[int, int]] | None
    nodes_expanded: int
    solved: bool = field(init=False)

    def __post_init__(self) -> None:
        self.solved = self.path is not None


def knights_tour(
    board_size: int,
    start: tuple[int, int] = (0, 0),
    use_warnsdorff: bool = True,
    node_limit: int = 500_000,
) -> KnightsTourResult:
    
    if board_size <= 0:
        raise ValueError(f"'board_size' must be positive, got {board_size}.")
    if not (0 <= start[0] < board_size and 0 <= start[1] < board_size):
        raise ValueError(f"Start square {start} is outside a {board_size}x{board_size} board.")

    board = [[False] * board_size for _ in range(board_size)]
    path: list[tuple[int, int]] = [start]
    board[start[0]][start[1]] = True
    nodes_expanded = 0

    def onward_degree(row: int, col: int) -> int:
        """Count unvisited squares reachable from ``(row, col)``."""
        count = 0
        for delta_row, delta_col in _KNIGHT_MOVES:
            new_row, new_col = row + delta_row, col + delta_col
            in_bounds = 0 <= new_row < board_size and 0 <= new_col < board_size
            if in_bounds and not board[new_row][new_col]:
                count += 1
        return count

    def backtrack(row: int, col: int, move_number: int) -> bool:
        nonlocal nodes_expanded
        nodes_expanded += 1
        if nodes_expanded > node_limit:
            return False
        if move_number == board_size * board_size:
            return True

        candidates = [
            (row + dr, col + dc)
            for dr, dc in _KNIGHT_MOVES
            if 0 <= row + dr < board_size
            and 0 <= col + dc < board_size
            and not board[row + dr][col + dc]
        ]
        if use_warnsdorff:
            candidates.sort(key=lambda square: onward_degree(*square))

        for next_row, next_col in candidates:
            board[next_row][next_col] = True
            path.append((next_row, next_col))
            if backtrack(next_row, next_col, move_number + 1):
                return True
            board[next_row][next_col] = False
            path.pop()
        return False

    found = backtrack(start[0], start[1], 1)
    return KnightsTourResult(path=path if found else None, nodes_expanded=nodes_expanded)