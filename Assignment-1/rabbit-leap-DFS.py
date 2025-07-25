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

def dfs(state, visited, path):
    if goal_state(state):
        return path
    visited.add(state)
    for move in move_gen(state):
        if move not in visited:
            result = dfs(move, visited, path + [move])
            if result is not None:
                return result
    return None

start = ('E', 'E', 'E', '_', 'W', 'W', 'W')
visited = set()
result = dfs(start, visited, [start])

for step in result:
    print(step)
