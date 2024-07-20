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
        for source in sources:
            queue.append((0, source[0], source[1]))  # (time_taken, x, y)
            self.distance[source[0]][source[1]] = 0

        while queue:
            current_time, current_x, current_y = queue.popleft()

            # If we reach the destination within the committed time, stop
            if self.map.cell_type(current_x, current_y) == DESTINATION and current_time <= self.map.time_commitment:
                return

            for direction in range(4):
                next_x, next_y = current_x + dx[direction], current_y + dy[direction]

                if not self.map.inside(next_x, next_y):
                    continue

                next_cell = self.map.matrix[next_x][next_y]

                if next_cell == WALL:
                    continue

                if next_cell in (NORMAL_CELL, SOURCE, DESTINATION):
                    move_time = 1
                elif next_cell == TOOL_BOOTH:
                    move_time = int(next_cell) + 1
                else:
                    continue

                new_time = current_time + move_time

                if new_time < self.distance[next_x][next_y] and new_time <= self.map.time_commitment:
                    self.distance[next_x][next_y] = new_time
                    self.trace[next_x][next_y] = (current_x, current_y)
                    queue.append((new_time, next_x, next_y))