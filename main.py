from level.level_2 import Level2
from object.map import Map

if __name__ == "__main__":
    _map = Map("temp_file/input_lv2.txt")
    level = Level2(_map)
    level.run()
