from level.level import Level
from algorithm.level_4_algo import *

class Level4(Level):
    def __init__(self, _map = None):
        super().__init__(_map)
    
    def run(self):
        if self.map is None:
            raise Exception("Map is not set in Level 4!")
        algorithm = Multiple_Agent_Algorithm(self.map)
        algorithm.run()
        path = algorithm.get_trace()
        print(len(self.map.get_list_matrix()))
        print(len(path[0]))
        # return (path, self.map.get_list_matrix())
        # print(self.map.get_list_matrix())
        return path