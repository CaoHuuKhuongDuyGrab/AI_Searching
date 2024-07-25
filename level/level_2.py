from level.level import Level
from algorithm.level_2_algo import *

class Level2(Level):
    def __init__(self, _map = None):
        super().__init__(_map)
    
    def run(self):
        if self.map is None:
            raise Exception("Map is not set in Level 2 !")
        algorithm = BFS_With_Time_Constrain(self.map)
        algorithm.run()
        path = algorithm.get_trace()
        return path
        # print(algorithm.algorithm_name)
        # self.print_path(path)
