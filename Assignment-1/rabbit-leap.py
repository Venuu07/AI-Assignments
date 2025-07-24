from collections import deque

def goal_state(state):
    return state == ('W', 'W', 'W', '_', 'E', 'E', 'E')

def move_gen(state):
    moves = []
    state = list(state)
    for i in range(len(state)):
        if state[i] == 'E':
            if i + 1 < len(state) and state[i + 1] == '_':
                new_state = state.copy()
                new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
                moves.append(tuple(new_state))
            elif i + 2 < len(state) and state[i + 2] == '_' and state[i + 1] in ('W', 'E'):
                new_state = state.copy()
                new_state[i], new_state[i + 2] = new_state[i + 2], new_state[i]
                moves.append(tuple(new_state))
        elif state[i] == 'W':
            if i - 1 >= 0 and state[i - 1] == '_':
                new_state = state.copy()
                new_state[i], new_state[i - 1] = new_state[i - 1], new_state[i]
                moves.append(tuple(new_state))
            elif i - 2 >= 0 and state[i - 2] == '_' and state[i - 1] in ('E', 'W'):
                new_state = state.copy()
                new_state[i], new_state[i - 2] = new_state[i - 2], new_state[i]
                moves.append(tuple(new_state))
    return moves

def bfs(start_state):
    visited = set()
    queue = deque()
    queue.append((start_state, [start_state]))
    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        if goal_state(current):
            return path
        for move in move_gen(current):
            if move not in visited:
                queue.append((move, path + [move]))
    return None

start = ('E', 'E', 'E', '_', 'W', 'W', 'W')
result = bfs(start)
for step in result:
    print(step)
