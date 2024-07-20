from collections import deque
from config.global_var import *
from algorithm.algorithm import Algorithm
import heapq

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

    def dfs(self, x):
        next_moves = self.map.next_move(x[0], x[1])
        for next_move in next_moves:
            if not self.map.inside(next_move[0], next_move[1]):
                continue
            if self.distance[next_move[0]][next_move[1]] == oo:
                self.distance[next_move[0]][next_move[1]] = True
                self.trace[next_move[0]][next_move[1]] = x
                self.dfs(next_move)

    def solve(self):
        # Implement depth-first search algorithm here
        source = self.map.get_sources()[0]
        self.distance[source[0]][source[1]] = True
        self.dfs(source)
        

class UniformCostSearch(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Uniform Cost Search")

    def solve(self):
        sources = self.map.get_sources()
        pq = []
        for source in sources:
            heapq.heappush(pq, (0, source))
            self.distance[source[0]][source[1]] = 0
        while pq:
            dist, current = heapq.heappop(pq)
            if self.distance[current[0]][current[1]] < dist:
                continue
            next_moves = self.map.next_move(current[0], current[1])
            for next_move in next_moves:
                if not self.map.inside(next_move[0], next_move[1]):
                    continue
                if self.distance[next_move[0]][next_move[1]] > self.distance[current[0]][current[1]] + 1:
                    self.distance[next_move[0]][next_move[1]] = self.distance[current[0]][current[1]] + 1
                    self.trace[next_move[0]][next_move[1]] = current
                    heapq.heappush(pq, (self.distance[next_move[0]][next_move[1]], next_move))

class AStarSearch(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "A* Algorithm")

    def solve(self):
        heuritic = [[0 for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)]
        destination = self.map.get_destinations()[0]
        for i in range(self.map.num_rows):
            for j in range(self.map.num_cols):
                heuritic[i][j] = abs(i - destination[0]) + abs(j - destination[1])
        
        pq = []
        sources = self.map.get_sources()
        for source in sources:
            heapq.heappush(pq, (heuritic[source[0]][source[1]], source))
            self.distance[source[0]][source[1]] = 0
        
        while pq:
            dist, current = heapq.heappop(pq)
            dist = dist - heuritic[current[0]][current[1]]
            if self.distance[current[0]][current[1]] < dist:
                continue
            next_moves = self.map.next_move(current[0], current[1])
            for next_move in next_moves:
                if not self.map.inside(next_move[0], next_move[1]):
                    continue
                if self.distance[next_move[0]][next_move[1]] > self.distance[current[0]][current[1]] + 1:
                    self.distance[next_move[0]][next_move[1]] = self.distance[current[0]][current[1]] + 1
                    self.trace[next_move[0]][next_move[1]] = current
                    heapq.heappush(pq, (self.distance[next_move[0]][next_move[1]] + heuritic[next_move[0]][next_move[1]], next_move))

class GreedyBestFirstSearch(Algorithm):
    def __init__(self, _map):
        super().__init__(_map, "Greedy Best First Search")

    def solve(self):
        heuritic = [[0 for _ in range(self.map.num_cols)] for _ in range(self.map.num_rows)]
        destination = self.map.get_destinations()[0]
        for i in range(self.map.num_rows):
            for j in range(self.map.num_cols):
                heuritic[i][j] = abs(i - destination[0]) + abs(j - destination[1])
        
        pq = []
        sources = self.map.get_sources()
        for source in sources:
            heapq.heappush(pq, (heuritic[source[0]][source[1]], source))
            self.distance[source[0]][source[1]] = True
        
        while pq:
            _, current = heapq.heappop(pq)
            next_moves = self.map.next_move(current[0], current[1])
            for next_move in next_moves:
                if not self.map.inside(next_move[0], next_move[1]):
                    continue
                if self.distance[next_move[0]][next_move[1]] == oo:
                    self.distance[next_move[0]][next_move[1]] = True
                    self.trace[next_move[0]][next_move[1]] = current
                    heapq.heappush(pq, (heuritic[next_move[0]][next_move[1]], next_move))
