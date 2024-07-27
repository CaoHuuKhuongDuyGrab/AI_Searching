from algorithm.algorithm import Algorithm
from config.global_var import *
from collections import deque

debug = False

class Multiple_Agent_Algorithm(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Multiple Agent Algorithm")
        self.path = None

    def add_destination(self, destination, destination_index):
        debug = (destination_index == 0)
        for x in range(self.map.num_rows):
            for y in range(self.map.num_cols):
                for time_commitment in range(self.map.time_commitment + 1):
                    for fuel in range(self.map.fuel + 1):
                        self.distance[destination_index][x][y][time_commitment][fuel] = oo
                        self.trace[destination_index][x][y][time_commitment][fuel] = []
        queue = deque()
        
        for time_commitment in range(self.map.time_commitment + 1):
            for fuel in range(self.map.fuel + 1):
                self.distance[destination_index][destination[0]][destination[1]][time_commitment][fuel] = 0
                queue.append((0, destination[0], destination[1], time_commitment, fuel))
            

        while queue:
            dist, current_x, current_y, current_time, current_fuel = queue.popleft()
            if self.distance[destination_index][current_x][current_y][current_time][current_fuel] < dist:
                continue
            next_moves = self.map.next_move(current_x, current_y)
            for next_move in next_moves:                
                next_x, next_y = next_move
                if not self.map.inside(next_x, next_y):
                    continue
                current_map = self.map
                cell_type = current_map.cell_type(current_x, current_y)
                if cell_type == SOURCE and current_map.get_order_cell(current_x, current_y) != destination_index:
                    current_map = current_map.origin_map
                    cell_type = current_map.cell_type(current_x, current_y)

                move_time = 1
                fuel_time = 0
                if cell_type == TOOL_BOOTH:
                    move_time += current_map.get_cell_value(current_x, current_y)

                new_fuel = current_fuel - 1
                if cell_type == GAS_STATION:
                    new_fuel = current_map.fuel - 1
                    fuel_time = int(current_map.matrix[current_x][current_y][1:])
                    
                new_time = current_time + move_time + fuel_time

                if new_fuel < 0:
                    continue
                if new_time > current_map.time_commitment:
                    continue

                new_distance = dist + 1
                self.trace[destination_index][next_x][next_y][new_time][new_fuel].append((current_x, current_y, current_time, current_fuel))

                if new_distance < self.distance[destination_index][next_x][next_y][new_time][new_fuel]:
                    self.distance[destination_index][next_x][next_y][new_time][new_fuel] = new_distance
                    queue.append((new_distance, next_x, next_y, new_time, new_fuel))

    def get_next_state(self, state, agent_index, current_time):

        min_distance = oo
        next_move = None
        source = state[0], state[1]
        _time = state[2]
        fuel = state[3]
        next_best_state = None
        next_states = self.trace[agent_index][source[0]][source[1]][_time][fuel]
        # if agent_index == 0:
        #     print(f"Check: {next_states}")
        for next_state in next_states:
            next_x, next_y = next_state[0], next_state[1]
            next_time = next_state[2]
            next_fuel = next_state[3]
            # if self.map.strongest_agent_can_pass(next_x, next_y) < agent_index:
            #     continue
            can_go = True
            for i in range(agent_index):
                if self.path[i][current_time][0] == next_x and self.path[i][current_time][1] == next_y:
                    can_go = False
                    break
            if can_go == False:
                continue
            if self.distance[agent_index][next_x][next_y][next_time][next_fuel] < min_distance:
                min_distance = self.distance[agent_index][next_x][next_y][next_time][next_fuel]
                next_best_state = next_state
        # if agent_index == 0:
        #     print(next_best_state)
        if next_best_state is None:
            if agent_index == 2:
                pass
            if _time - 1 < 0: 
                print("Time problem !")
                # raise Exception(f"Agent index: {agent_index} got the Time problem")
                return
            self.path[agent_index].append((source[0], source[1], _time - 1, fuel))
            return
        next_move = next_best_state[0], next_best_state[1]
        new_time = next_best_state[2]
        new_fuel = next_best_state[3]
        waiting_time = 0
        new_cell_type = self.map.cell_type(next_move[0], next_move[1])
        current_map = self.map
        if new_cell_type == SOURCE and self.map.get_order_cell(next_move[0], next_move[1]) != agent_index:
            new_cell_type = self.map.origin_map.cell_type(next_move[0], next_move[1])
            current_map = self.map.origin_map
        if new_cell_type == GAS_STATION:
            waiting_time = current_map.get_order_cell(next_move[0], next_move[1])
        elif new_cell_type == TOOL_BOOTH:
            waiting_time = current_map.get_cell_value(next_move[0], next_move[1])
        # print("HWEHUWEHUW" + str(waiting_time))
        for _ in range(waiting_time + 1):
            self.path[agent_index].append((next_move[0], next_move[1], new_time, new_fuel))
    
    def update_map(self, current_time):
        sources = self.map.get_sources()
        destinations = self.map.get_destinations()
        done = [False for _ in range(self.num_agents)]
        for agent_index, source in enumerate(sources):
            if self.map.cell_type(source[0], source[1]) == DESTINATION and self.map.get_order_cell(source[0], source[1]) == agent_index:
                done[agent_index] = True
            self.map.matrix[source[0]][source[1]] = self.map.origin_map.matrix[source[0]][source[1]]
        for agent_index in range(self.num_agents):
            source = self.path[agent_index][current_time]
            self.map.matrix[source[0]][source[1]] = "S"
            if agent_index > 0:
                self.map.matrix[source[0]][source[1]] += str(agent_index)
                if done[agent_index]:
                    random_cell = self.map.get_valid_cell()
                    self.map.matrix[random_cell[0]][random_cell[1]] = "F" + str(agent_index)
                    self.add_destination(random_cell, agent_index)
            elif done[0] == True :
                return True



    def solve(self):
        sources = self.map.get_sources()
        destinations = self.map.get_destinations()
        self.num_agents = len(sources)
        self.distance = [[[[[oo for _ in range(self.map.fuel + 1)] for _ in range(self.map.time_commitment + 1)] for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)] for _ in range(self.num_agents)]
        self.trace = [[[[[[] for _ in range(self.map.fuel + 1)] for _ in range(self.map.time_commitment + 1)] for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)] for _ in range(self.num_agents)]
        for index, destination in enumerate(destinations):
            self.add_destination(destination, index)
            # print(self.distance[0][1][1][20][10])
            # return
        # print(self.distance[0])
        # print(self.trace[0][1][1][20][4])
        # return
        self.path = [[] for i in range(self.num_agents)]
        for index, source in enumerate(sources):
            Min = oo
            _time_ = None
            _fuel_ = None
            for _time in range(self.map.time_commitment + 1):
                for _fuel in range(1, self.map.fuel + 1):
                    if self.distance[index][source[0]][source[1]][_time][_fuel] < Min:
                        Min = self.distance[index][source[0]][source[1]][_time][_fuel]
                        _time_ = _time
                        _fuel_ = _fuel
            self.path[index].append((source[0], source[1], _time_, _fuel_))
        cnt_time = 0
        while True:
            for i in range(self.num_agents):
                if len(self.path[i]) <= cnt_time:
                    return
            for index in range(self.num_agents):
                if cnt_time + 1 == len(self.path[index]):
                    self.get_next_state(self.path[index][-1], index, cnt_time + 1)
                    # if index == 2:
                    #     print(self.path[index][-1], len(self.path[index]))
            if self.update_map(cnt_time) == True:
                print("Reached the goal")
                return
            cnt_time += 1
            print(cnt_time)
            self.map.print_2d_array()

    def get_trace(self):
        if self.path == None:
            return -1
        return self.path
            