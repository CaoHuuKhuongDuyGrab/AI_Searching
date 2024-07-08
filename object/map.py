from configg.global_var import *

class Map:
    def __init__(self, num_rows, num_cols, time_commitment, fuel, matrix = None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.time_commitment = time_commitment
        self.fuel = fuel
        self.matrix = matrix
    
    def inside(self, row, col):
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            return False
        if self.matrix[row][col] == WALL:
            return False
        return True

    def load_map(self):
        for _ in range(self.num_rows):
            row = input().split()
            self.matrix.append(row)
