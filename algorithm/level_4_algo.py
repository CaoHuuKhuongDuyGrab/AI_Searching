from algorithm.algorithm import Algorithm
from config.global_var import *
from collections import deque
import copy

debug = False

class Multiple_Agent_Algorithm(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Multiple Agent Algorithm")
        self.path = None

    def get_next_state_all(self, state, agent_index, debug = False):
        current_x, current_y, current_time, current_fuel = state
        next_moves = self.map.next_move(current_x, current_y)
        next_states = []
        # if debug:
        #     print(f"Debug state: {state}")
        for next_move in next_moves:                
            next_x, next_y = next_move
            if not self.map.inside(next_x, next_y):
                continue
            current_map = self.map
            cell_type = current_map.cell_type(current_x, current_y)
            if (cell_type == DESTINATION and current_map.get_order_cell(current_x, current_y) != agent_index) or cell_type == SOURCE:
                current_map = current_map.origin_map
                cell_type = current_map.cell_type(current_x, current_y)

            move_time = 1
            fuel_time = 0
            if debug:
                print(f"Cell type: {cell_type} {self.map.matrix[current_x][current_y]}")
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
            next_states.append((next_x, next_y, new_time, new_fuel))
        return next_states

    def get_heuristic(self, state, source_index):
        debug = (state == (7, 3, 7, 3) and source_index == 1)
        self.distance = [[[[oo for _ in range(self.map.fuel + 1)] for _ in range(self.map.time_commitment + 1)] for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)]

        for x in range(self.map.num_rows):
            for y in range(self.map.num_cols):
                for time_commitment in range(self.map.time_commitment + 1):
                    for fuel in range(self.map.fuel + 1):
                        self.distance[x][y][time_commitment][fuel] = oo
                        # self.trace[destination_index][x][y][time_commitment][fuel] = []
        queue = deque()
        self.distance[state[0]][state[1]][state[2]][state[3]] = 0
        queue.append((0, state[0], state[1], state[2], state[3]))

        while queue:
            dist, current_x, current_y, current_time, current_fuel = queue.popleft()
            if self.distance[current_x][current_y][current_time][current_fuel] < dist:
                continue
            next_moves = self.map.next_move(current_x, current_y)
            for next_move in next_moves:                
                next_x, next_y = next_move
                if not self.map.inside(next_x, next_y):
                    continue
                current_map = self.map
                cell_type = current_map.cell_type(current_x, current_y)
                # if (cell_type == DESTINATION or cell_type == SOURCE) and current_map.get_order_cell(current_x, current_y) != source_index:
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
                # self.trace[next_x][next_y][new_time][new_fuel].append((current_x, current_y, current_time, current_fuel))

                if new_distance < self.distance[next_x][next_y][new_time][new_fuel]:
                    self.distance[next_x][next_y][new_time][new_fuel] = new_distance
                    queue.append((new_distance, next_x, next_y, new_time, new_fuel))
        res = oo
         
        for destination in self.map.get_destinations():
            if self.map.get_order_cell(destination[0], destination[1]) == source_index:
                for time_commitment in range(self.map.time_commitment + 1):
                    for fuel in range(self.map.fuel + 1):
                        res = min(res, self.distance[destination[0]][destination[1]][time_commitment][fuel])
        # print(state, res, source_index)
        if debug:
            print("debug destination")
            # print(self.map.origin_map.cell_type(6, 2))
            # print(self.map.origin_map.matrix[6][2])
            print(self.distance[7][2][8][2])
            print(self.distance[6][2][9][1])
            print(self.distance[6][1][10][9])
            print(res)
            # print(self.map.get_destinations())
            # print(self.map.get_order_cell(4, 5, True))
            print("End debug") 
        return res

    def get_next_state(self, state, agent_index, current_time):
        min_distance = oo
        next_move = None
        next_best_state = None
        next_states = self.get_next_state_all(state, agent_index)
        # print(next_states)
        # print("hello")
        debug = (agent_index == 1 and current_time == 7)
        if debug:
            print(f"Current state: {state}")
            print(self.get_next_state_all(state, agent_index, True))
        for next_state in next_states:
            can_move = True
            if debug:
                print(f"Next state: {next_state}")
                print(f"Value: {self.get_heuristic(next_state, agent_index)}")
            for agent in range(self.num_agents):
                try:
                    if agent < agent_index and self.path[agent][current_time][0] == next_state[0] and self.path[agent][current_time][1] == next_state[1]:
                        can_move = False
                    if current_time > 0:
                        if self.path[agent][current_time - 1][0] == next_state[0] and self.path[agent][current_time - 1][1] == next_state[1]:
                            can_move = False
                except:
                    # print(f"debug: {current_time} {state[2]} {agent_index}")
                    # print(self.get_next_state_all((6, 5, 2, 8), agent_index))
                    # print(self.path[agent_index])
                    exit(0)
            if can_move == False:
                continue
            heuristic = self.get_heuristic(next_state, agent_index)
            if heuristic < min_distance:
                min_distance = heuristic
                next_best_state = next_state
        if debug:
            print(f"Best state {next_best_state}")
        if next_best_state == None:
            if state[2] + 1 > self.map.time_commitment:
                return
            self.path[agent_index].append((state[0], state[1], state[2] + 1, state[3]))
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
    
    def update_map(self, current_time, fo):
        sources = self.map.get_sources()
        destinations = self.map.get_destinations()
        debug = (current_time == 2)

        done = [False for _ in range(self.num_agents)]

        for agent_index, source in enumerate(sources):
            if self.map.cell_type(source[0], source[1]) == DESTINATION and self.map.get_order_cell(source[0], source[1]) == agent_index:
                self.map.matrix[source[0]][source[1]] = "0"
                self.map.origin_map.matrix[source[0]][source[1]] = "0"
            self.map.matrix[source[0]][source[1]] = self.map.origin_map.matrix[source[0]][source[1]]
        try:
            for agent_index in range(self.num_agents):
                source = self.path[agent_index][current_time]
                if self.map.cell_type(source[0], source[1]) == DESTINATION and self.map.get_order_cell(source[0], source[1]) == agent_index:
                    done[agent_index] = True
                self.map.matrix[source[0]][source[1]] = "S"
                # if debug:
                #     print(source)
                if agent_index > 0:
                    self.map.matrix[source[0]][source[1]] += str(agent_index)
                    if done[agent_index]:
                        print(f"Agent {agent_index} reached the goal at time {current_time}")
                        random_cell = self.map.get_valid_cell()
                        print(f"New destination for agent {agent_index}: {random_cell}")
                        self.map.matrix[random_cell[0]][random_cell[1]] = "G" + str(agent_index)
                        self.map.origin_map.matrix[random_cell[0]][random_cell[1]] = "G" + str(agent_index)
                        self.map.origin_map.matrix[source[0]][source[1]] = "0"
                        done[agent_index] = False
                        fo.write(f"{current_time} {random_cell[0]} {random_cell[1]} {"G" + str(agent_index)}\n")
                        # self.add_destination(random_cell, agent_index)
        except:
            print(f"Sai o dau do{current_time}")
            # print(e)
        # self.map.list_matrix.append(self.map.matrix)
        # deepcopy_matrix = copy.deepcopy(self.map.matrix)
        self.map.list_matrix.append(copy.deepcopy(self.map.matrix))
        if done[0] == True:                      
            return True
        

    def solve(self):
        sources = self.map.get_sources()
        destinations = self.map.get_destinations()
        self.num_agents = len(sources)

        self.path = [[] for i in range(self.num_agents)]
        for index, source in enumerate(sources):
            self.path[index].append((source[0], source[1], 0, self.map.fuel))

        cnt_time = 0
        fo = open("algorithm/new_des.txt", "w")

        try:
            while True:
                for i in range(self.num_agents):
                    if len(self.path[i]) <= cnt_time:
                        break
                cnt_time += 1
                for index in range(self.num_agents):
                    # print(cnt_time, self.path[index])
                    if cnt_time == len(self.path[index]):
                        self.get_next_state(self.path[index][-1], index, cnt_time)
                        # if index == 2:
                        #     print(self.path[index][-1], len(self.path[index]))
                
                print(cnt_time)
                if self.update_map(cnt_time, fo) == True:
                    print("Reached the goal")
                    break
                
                self.map.print_2d_array()
                if cnt_time >= self.map.time_commitment:
                    print("Time out")
                    break
                # for i in range(self.num_agents):
                #     print(f"Agent {i}: {self.path[i]}")
        except :
            print(f"Error at time {cnt_time}")
            # print(e)
        print("ENDDD")
        fo.close()


    def get_trace(self):
        if self.path == None:
            return -1
        trace_path = []
        for i in range(self.num_agents):
            trace_path.append([])
            for j in range(len(self.path[i])):
                trace_path[i].append(self.path[i][j][:2])
        print(trace_path)
        return trace_path
            