import heapq

def is_valid(grid, row, col):
    n = len(grid)
    if row >= 0 and row < n and col >= 0 and col < n and grid[row][col] == 0:
        return True
    return False

def get_neighbors(row, col):
    return [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1), (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    return path[::-1]

def best_first_search(grid):
    n = len(grid)
    start = (0, 0)
    goal = (n - 1, n - 1)

    if grid[start[0]][start[1]] == 1:
        return -1, []

    frontier = [(manhattan_distance(start, goal), start)]
    came_from = {start: None}
    visited = {start}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return len(path), path

        for neighbor in get_neighbors(current[0], current[1]):
            if is_valid(grid, neighbor[0], neighbor[1]) and neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                priority = manhattan_distance(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))

    return -1, []

def a_star_search(grid):
    n = len(grid)
    start = (0, 0)
    goal = (n - 1, n - 1)

    if grid[start[0]][start[1]] == 1:
        return -1, []

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return len(path), path

        for neighbor in get_neighbors(current[0], current[1]):
            new_cost = cost_so_far[current] + 1
            if is_valid(grid, neighbor[0], neighbor[1]):
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + manhattan_distance(neighbor, goal)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

    return -1, []

def solve(grid):
    print("Best First Search")
    length, path = best_first_search(grid)
    print(f"Path length: {length}, Path: {path}")

    print("A* Search")
    length, path = a_star_search(grid)
    print(f"Path length: {length}, Path: {path}")
    print("-" * 20)

# Example 1
grid1 = [[0, 1], [1, 0]]
print("--- Example 1 ---")
solve(grid1)

# Example 2
grid2 = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
print("--- Example 2 ---")
solve(grid2)

# Example 3
grid3 = [[1, 0, 0], [1, 1, 0], [1, 1, 0]]
print("--- Example 3 ---")
solve(grid3)