"""
Robot grid

Find the shortest path through the grid from top left to bottom right.

grid = [
  [1, 1, 1, 1, 1],
  [1, 0, 1, 0, 0],
  [1, 0, 1, 1, 1],
  [1, 1, 1, 0, 1],
]


Approach
--------

At each point we can move in one of four directions
"""


def is_valid(position, grid):
    row, col = position
    n_rows = len(grid)
    n_cols = len(grid[0])

    if 0 <= row < n_rows and 0 <= col < n_cols:
        if grid[row][col]:
            return True

    return False


def is_end(position, grid):
    return position[0] == len(grid) - 1 and position[1] == len(grid[0]) - 1


def move_right(current_position: tuple[int, int], grid: list[list[int]]):
    return (current_position[0], current_position[1] + 1)


def move_down(current_position: tuple[int, int], grid: list[list[int]]):
    return (current_position[0] + 1, current_position[1])


ALL_MOVES = [
    move_down,
    move_right,
]


def find_path(grid):
    # Store visited positions and number of steps to get there.
    # Maybe better to store the path itself?
    visited = {}
    yield from _dfs([(0, 0)], grid, visited)


def _dfs(path, grid, visited):
    if is_end(path[-1], grid):
        yield path
    else:
        for move in ALL_MOVES:
            new_position = move(path[-1], grid)
            if is_valid(new_position, grid):
                if new_position not in visited or len(path) + 1 < visited[new_position]:
                    visited[new_position] = len(path) + 1
                    yield from _dfs(path + [new_position], grid, visited)


def test_find_path():
    grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0],
        [1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1],
    ]

    path = list(find_path(grid))

    print(path)
