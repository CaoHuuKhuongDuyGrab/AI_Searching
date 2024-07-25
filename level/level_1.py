from level.level import Level
from algorithm.level_1_algo import *

class Level1(Level):
    def __init__(self, _map = None):
        super().__init__(_map)

    def run(self):
        if self.map is None:
            raise Exception("Map is not set in Level1")
        algorithm1 = BreadthFirstSearch(self.map)
        algorithm1.run()
        path1 = algorithm1.get_trace()
        # print(algorithm.algorithm_name)
        # self.print_path(path)

        algorithm2 = DepthFirstSearch(self.map)
        algorithm2.run()
        path2 = algorithm2.get_trace()
        # print(algorithm.algorithm_name)
        # self.print_path(path)

        algorithm3 = UniformCostSearch(self.map)
        algorithm3.run()
        path3 = algorithm3.get_trace()
        # print(algorithm.algorithm_name)
        # self.print_path(path)

        algorithm4 = GreedyBestFirstSearch(self.map)
        algorithm4.run()
        path4 = algorithm4.get_trace()
        # print(algorithm.algorithm_name)
        # self.print_path(path)

        algorithm5 = AStarSearch(self.map)
        algorithm5.run()
        path5 = algorithm5.get_trace()
        # print(algorithm.algorithm_name)
        # self.print_path(path)

        return path1, path2, path3, path4, path5

