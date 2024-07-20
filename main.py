from level.level_1 import Level1
from object.map import Map

if __name__ == "__main__":
    _map = Map("temp_file/input_lv1.txt")
    level = Level1(_map)
    level.run()
