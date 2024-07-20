
class Level:
    def __init__(self, _map = None):
        self.map = _map

    def set_map(self, _map):
        self.map = _map
    
    def print_path(self, path):
        for i in range(len(path)):
            print(path[i], end=" ")
        print()

    def run(self):
        pass
    