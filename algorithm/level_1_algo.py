from collections import deque
from config.global_var import *
from algorithm.algorithm import Algorithm

class BreadthFirstSearch(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Breadth First Search")
    def solve(self):
        # Implement breadth-first search algorithm here
        queue = deque()
        sources = self.map.get_sources()
        for source in sources:
            queue.append(source)
            self.distance[source[0]][source[1]] = 0
        while queue:
            current = queue.popleft()
            next_moves = self.map.next_move(current[0], current[1])
            for next_move in next_moves:
                if not self.map.inside(next_move[0], next_move[1]):
                    continue
                if self.distance[next_move[0]][next_move[1]] == oo:
                    self.distance[next_move[0]][next_move[1]] = self.distance[current[0]][current[1]] + 1
                    self.trace[next_move[0]][next_move[1]] = current
                    queue.append(next_move)
        

class DepthFirstSearch(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Depth First Search")

    def solve(self):
        # Implement depth-first search algorithm here
        pass

class UniformCostSearch(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Uniform Cost Search")

    def solve(self):
        # Implement Dijkstra's algorithm here
        pass

class AStarAlgorithm(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "A* Algorithm")

    def solve(self):
        # Implement A* algorithm here
        pass

class GreedyBestFirstSearch(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Greedy Best First Search")

    def solve(self):
        # Implement greedy best-first search algorithm here
        pass
