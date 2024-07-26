from level.level import Level

class Level3(Level):
    def __init__(self, _map = None):
        super().__init__(_map)
    
    def run(self):
        if self.map is None:
            raise Exception("Map is not set in Level 4!")
        algorithm = BFS_With_Time_Fuel_Constrain(self.map)
        algorithm.run()
        path = algorithm.get_trace()
        return path