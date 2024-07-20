from level.level import Level
from algorithm.level_1_algo import *

class Level1(Level):
    def __init__(self, _map = None):
        super().__init__(_map)

    def run(self):
        if self.map is None:
            raise Exception("Map is not set in Level1")
        algorithm = BreadthFirstSearch(self.map)
        algorithm.run()
        path = algorithm.get_trace()
        print(algorithm.algorithm_name)
        self.print_path(path)

        algorithm = DepthFirstSearch(self.map)
        algorithm.run()
        path = algorithm.get_trace()
        print(algorithm.algorithm_name)
        self.print_path(path)

        algorithm = UniformCostSearch(self.map)
        algorithm.run()
        path = algorithm.get_trace()
        print(algorithm.algorithm_name)
        self.print_path(path)

        algorithm = GreedyBestFirstSearch(self.map)
        algorithm.run()
        path = algorithm.get_trace()
        print(algorithm.algorithm_name)
        self.print_path(path)

        algorithm = AStarSearch(self.map)
        algorithm.run()
        path = algorithm.get_trace()
        print(algorithm.algorithm_name)
        self.print_path(path)


