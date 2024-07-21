from collections import deque
from config.global_var import *
from algorithm.algorithm import Algorithm
import heapq

class BFS_With_Time_Constrain(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Breadth First Search with Time Constraint")

    def solve(self):
        queue = deque()
        sources = self.map.get_sources()
        self.distance = [[[oo for _ in range(self.map.time_commitment + 1)] for _ in range(self.map.num_cols + 1)] for _ in range(self.map.num_rows + 1)]
        self.trace = [[[None for _ in range(self.map.time_commitment + 1)] for _ in range(self.map.num_cols + 1)] for _ in range(self.map.num_rows + 1)]
        for source in sources:
            queue.append((0, source[0], source[1], 0))
            self.distance[source[0]][source[1]][0] = 0

        while queue:
            dist, current_x, current_y, current_time = queue.popleft()
            if self.map.cell_type(current_x, current_y) == DESTINATION and current_time <= self.map.time_commitment:
                return

            next_moves = self.map.next_move(current_x, current_y)

            for next_move in next_moves:

                next_x, next_y = next_move
                if not self.map.inside(next_x, next_y):
                    continue
                
                cell_type = self.map.cell_type(current_x, current_y)

                if not self.map.inside(next_x, next_y): 
                    continue

                move_time = 1
                if cell_type == TOOL_BOOTH:
                    move_time += self.map.get_cell_value(current_x, current_y)

                new_time = current_time + move_time
                if new_time > self.map.time_commitment:
                    continue
                new_distance = dist + 1
                if new_distance < self.distance[next_x][next_y][new_time]:
                    self.distance[next_x][next_y][new_time] = new_distance
                    self.trace[next_x][next_y][new_time] = (current_x, current_y, current_time)
                    queue.append((new_distance, next_x, next_y, new_time))


    def get_trace(self):
        current_pos = self.map.get_destinations()[0]
        _time = None
        Min = oo
        for _time_ in range(self.map.time_commitment + 1):
            if self.distance[current_pos[0]][current_pos[1]][_time_] < Min:
                Min = self.distance[current_pos[0]][current_pos[1]][_time_]
                _time = _time_
        
        if _time == None:
            return -1
        # goal state (x, y, _time)
        path = []
        while True:
            path.append(current_pos)
            previous_state = self.trace[current_pos[0]][current_pos[1]][_time]
            if previous_state == None:
                break
            current_pos = previous_state[:2]
            _time = previous_state[2]
        path.reverse()
        return path

                