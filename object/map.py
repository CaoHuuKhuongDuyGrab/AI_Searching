from config.global_var import *
import random
import copy

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class Map:
    def __init__(self, file_path = None):
        self.num_rows = None
        self.num_cols = None
        self.time_commitment = None
        self.fuel = None
        self.matrix = None
        self.origin_map = None
        if file_path is not None:
            self.load_map(file_path)
    
    def inside(self, row, col):
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            return False
        if self.cell_type(row, col) == WALL:
            return False
        return True

    def get_cell_value(self, row, col):
        if is_number(self.matrix[row][col]):
            return int(self.matrix[row][col])
        return self.matrix[row][col]

    def load_map(self, file_path):
        with open(file_path, "r") as f:
            self.num_rows, self.num_cols, self.time_commitment, self.fuel = map(int, f.readline().split())
            self.matrix = []
            for _ in range(self.num_rows):
                row = f.readline().split()
                self.matrix.append(row)
        tmp_matrix = []
        for i in range(self.num_rows):
            tmp = []
            for j in range(self.num_cols):
                if self.cell_type(i, j) == SOURCE or self.cell_type(i, j) == DESTINATION:
                    tmp.append(0)
                tmp.append(self.matrix[i][j])
            tmp_matrix.append(tmp)
        self.origin_map = copy.deepcopy(self)  
        self.origin_map.matrix = tmp_matrix
    
    def get_valid_cell(self):
        valid_cells = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.origin_map.cell_type(i, j) != WALL:
                    valid_cells.append((i, j))
        random_cell = random.choice(valid_cells)
        return random_cell

    def get_order_cell(self, row, col):
        if self.cell_type(row, col) != SOURCE and self.cell_type(row, col) != DESTINATION and self.cell_type(row, col) != GAS_STATION:
            return -1
        if len(self.matrix[row][col]) == 1:
            return 0
        return int(self.matrix[row][col][1:])
    
    def get_sources(self):
        sources = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.cell_type(i, j) == SOURCE:
                    sources.append((i, j))
        sources.sort(key = lambda x: self.get_order_cell(x[0], x[1]))
        return sources

    def get_destinations(self):
        destinations = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.cell_type(i, j) == DESTINATION:
                    destinations.append((i, j))
        destinations.sort(key = lambda x: self.get_order_cell(x[0], x[1]))
        return destinations
    
    def strongest_agent_can_pass(self, row, col):
        next_moves = self.next_move(row, col)
        Min = 100
        next_moves.append((row, col))
        for next_move in next_moves:
            if self.cell_type(next_move[0], next_move[1]) != SOURCE:
                continue
            tmp = self.get_order_cell(next_move[0], next_move[1])
            if tmp != -1 and tmp < Min:
                Min = tmp
        return Min
    
    def cell_type(self, row, col):
        if is_number(self.matrix[row][col]):
            if int(self.matrix[row][col]) == -1:
                return WALL
            if int(self.matrix[row][col]) > 0:
                return TOOL_BOOTH
            else:
                return NORMAL_CELL
            
        c = self.matrix[row][col][0]
        if c == "S":
            return SOURCE
        if c == "F":
            return GAS_STATION
        return DESTINATION

    def next_move(self, row, col):
        next_move_list = []
        for i in range(4):
            new_row = row + dx[i]
            new_col = col + dy[i]
            if self.inside(new_row, new_col):
                next_move_list.append((new_row, new_col))
        return next_move_list
    
    def print_2d_array(self):
        print("================================")
        print()
        for row in self.matrix:
            print(" ".join(f"{elem:5}" for elem in row))
        print()
        print("================================")