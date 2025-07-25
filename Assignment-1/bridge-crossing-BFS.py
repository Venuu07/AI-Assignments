from collections import deque

class BridgeCrossing:
    def __init__(self):
        self.times = {
            'Amogh': 5,
            'Ameya': 10,
            'Grandmother': 20,
            'Grandfather': 25
        }

    def is_goal_state(self, state):
        return len(state['start']) == 0 and state['time'] <= 60

    def get_possible_moves(self, state):
        next_states = []
        current_side = state['start'] if state['umbrella'] == 'start' else state['end']

        if state['umbrella'] == 'start':
            for i in range(len(current_side)):
                for j in range(i + 1, len(current_side)):
                    p1, p2 = current_side[i], current_side[j]
                    time_to_cross = max(self.times[p1], self.times[p2])
                    new_start = state['start'].copy()
                    new_end = state['end'].copy()
                    new_start.remove(p1)
                    new_start.remove(p2)
                    new_end.extend([p1, p2])
                    next_states.append({
                        'start': new_start,
                        'end': new_end,
                        'umbrella': 'end',
                        'time': state['time'] + time_to_cross
                    })
        else:
            for i in range(len(current_side)):
                p = current_side[i]
                time_to_return = self.times[p]
                new_start = state['start'].copy()
                new_end = state['end'].copy()
                new_end.remove(p)
                new_start.append(p)
                next_states.append({
                    'start': new_start,
                    'end': new_end,
                    'umbrella': 'start',
                    'time': state['time'] + time_to_return
                })

        return next_states

    def can_cross_in_time(self):
        initial_state = {
            'start': ['Amogh', 'Ameya', 'Grandmother', 'Grandfather'],
            'end': [],
            'umbrella': 'start',
            'time': 0
        }

        queue = deque()
        queue.append(initial_state)
        visited = set()

        while queue:
            current_state = queue.popleft()
            start_side = tuple(sorted(current_state['start']))
            end_side = tuple(sorted(current_state['end']))
            state_key = (start_side, end_side, current_state['umbrella'])

            if state_key in visited or current_state['time'] > 60:
                continue
            visited.add(state_key)

            if self.is_goal_state(current_state):
                return True

            for next_state in self.get_possible_moves(current_state):
                queue.append(next_state)

        return False

solver = BridgeCrossing()
if solver.can_cross_in_time():
    print("Yes, they can cross the bridge within 60 minutes.")
else:
    print("No, it's not possible within the time limit.")
