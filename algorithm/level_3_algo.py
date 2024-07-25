from collections import deque
from config.global_var import *
from algorithm.algorithm import Algorithm
import heapq

class BFS_With_Time_Fuel_Constrain(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Breadth First Search with Time And Fuel Constraint")

    def solve(self):
        queue = deque()
        sources = self.map.get_sources()
    
        self.distance = [[[[oo for _ in range(self.map.fuel + 1)] for _ in range(self.map.time_commitment + 1)] for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)]
        self.trace = [[[[None for _ in range(self.map.fuel + 1)] for _ in range(self.map.time_commitment + 1)] for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)]

        for source in sources:
            queue.append((0, source[0], source[1], 0, self.map.fuel))
            self.distance[source[0]][source[1]][0][self.map.fuel] = 0
            

        while queue:
            dist, current_x, current_y, current_time, current_fuel = queue.popleft()
            if self.map.cell_type(current_x, current_y) == DESTINATION and current_time <= self.map.time_commitment:
                # print(f"Destination found at ({current_x}, {current_y}) with Time: {current_time}, Fuel: {current_fuel}, Distance: {dist}")
                return

            next_moves = self.map.next_move(current_x, current_y)

            for next_move in next_moves:

                next_x, next_y = next_move
                if not self.map.inside(next_x, next_y):
                    continue
                
                cell_type = self.map.cell_type(current_x, current_y)

                # if not self.map.inside(next_x, next_y): 
                #     continue

                move_time = 1
                fuel_time = 0
                if cell_type == TOOL_BOOTH:
                    move_time += self.map.get_cell_value(current_x, current_y)

                new_fuel = current_fuel - 1
                if cell_type == GAS_STATION:
                    new_fuel = self.map.fuel
                    fuel_time = int(self.map.matrix[current_x][current_y][1:])
                    
                new_time = current_time + move_time + fuel_time

                if new_fuel <= 0:
                    continue
                if new_time > self.map.time_commitment:
                    continue

                new_distance = dist + 1

                if new_distance < self.distance[next_x][next_y][new_time][new_fuel]:
                    self.distance[next_x][next_y][new_time][new_fuel] = new_distance
                    self.trace[next_x][next_y][new_time][new_fuel] = (current_x, current_y, current_time, current_fuel)
                    queue.append((new_distance, next_x, next_y, new_time, new_fuel))

    def get_trace(self):
        current_pos = self.map.get_destinations()[0]
        _time = None
        _fuel = None
        Min = oo

        for _time_ in range(self.map.time_commitment + 1):
            for fuel in range(1, self.map.fuel + 1):
                if self.distance[current_pos[0]][current_pos[1]][_time_][fuel] < Min:
                    Min = self.distance[current_pos[0]][current_pos[1]][_time_][fuel]
                    _time = _time_
                    _fuel = fuel
        
        if _time == None:
            print("Time problem !")
            return -1
        if _fuel == None:
            print("Fuel problem !")
            return -1
        
        # goal state (x, y, _time)
        path = []
        while True:
            path.append(current_pos)
            previous_state = self.trace[current_pos[0]][current_pos[1]][_time][_fuel]
            if previous_state == None:
                break
            current_pos = previous_state[:2]
            _time = previous_state[2]
            _fuel = previous_state[3]
        path.reverse()
        return path

                