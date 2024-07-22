from level.level_3 import Level3
from object.map import Map
from gui import GUI



path = [
    "(1, 1) (2, 1) (3, 1) (4, 1) (5, 1) (6, 1) (6, 2) (6, 3) (5, 3) (5, 4) (5, 5) (6, 5) (7, 5) (7, 6) (7, 7) (7, 8)",    
        ]


if __name__ == "__main__":
    # _map = Map("temp_file/input_lv3.txt")
    # print(_map.get_sources())
    # level = Level3(_map)
    # level.run()


    gui = GUI('input.txt', path)
    gui.execute()
