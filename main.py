from level.level_3 import Level3
from object.map import Map

if __name__ == "__main__":
    _map = Map("temp_file/input_lv3.txt")
    # print(_map.get_sources())
    level = Level3(_map)
    level.run()
