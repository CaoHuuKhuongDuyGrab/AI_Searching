from config.global_var import *

class Algorithm:
    def __init__(self, _map, algorithm_name = None):
        self.map = _map
        self.trace = None
        self.distance = None
        self.algorithm_name = algorithm_name

    def run(self):
        self.trace = [[None for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)]
        self.distance = [[oo for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)]
        self.solve()

    def get_trace(self):
        destinations = self.map.get_destinations()
        for destination in destinations:
            if self.distance[destination[0]][destination[1]] == oo:
                return -1
            current = destination
            path = []
            while current is not None:
                path.append(current)
                current = self.trace[current[0]][current[1]]
            path.reverse()
        
        if len(destinations) == 1:
            return path
    
    def solve(self):
        pass