import algorithm.shortest_path
from config import global_var

class BreadthFirstSearch(algorithm.shortest_path.ShortestPath):
    def solve(self):
        pass

class DepthFirstSearch(algorithm.shortest_path.ShortestPath):
    def solve(self):
        # Implement depth-first search algorithm here
        pass

class UniformCostSearch(algorithm.shortest_path.ShortestPath):
    def solve(self):
        # Implement Dijkstra's algorithm here
        pass

class AStarAlgorithm(algorithm.shortest_path.ShortestPath):
    def solve(self):
        # Implement A* algorithm here
        pass

class GreedyBestFirstSearch(algorithm.shortest_path.ShortestPath):
    def solve(self):
        # Implement greedy best-first search algorithm here
        pass

if __name__ == "__main__":
    # Create an instance of the desired searching algorithm
    algorithm = BreadthFirstSearch()

    # Call the search method to perform the search
    algorithm.solve()