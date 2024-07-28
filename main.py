
from level.level_1 import Level1
from level.level_2 import Level2
from level.level_3 import Level3
from level.level_4 import Level4

from object.map import Map
from gui import GameScreen, ScreenManager, MenuScreen
import pygame
from ultils import convert_tuples_to_strings


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SIDEBAR_WIDTH = 300
SIDEBAR_HEIGHT = 600

MAP_WIDTH = 900
MAP_HEIGHT = 600
# path = [
#     "(4, 1) (4, 2) (4, 3) (4, 4) (4, 5) (4, 6) (4, 7) (4, 8 ) (5, 8 ) (5, 9) (5, 10) (5, 11) (5, 12) (5, 13) (6, 13) (6, 14) (6, 15) (6, 16) (7, 16) (7, 17) (7, 18) (7, 19) (8, 19) (9, 19) (10, 19) (11, 19) (12, 19) (13, 19) (14, 19) (15, 19) (15, 20) (16, 20) (17, 20) (18, 20) (18, 21) (18, 22) (19, 22) (20, 22)",
#     "(1, 2) (1, 3) (1, 4) (1, 5) (2, 5)",
#     "(1, 3) (1, 4) (1, 5)",
#     "(1, 4) (1, 5) (1, 6)",
#     "(1, 5) (1, 6) (1, 7)"
#         ]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_manager =  ScreenManager(screen)
    running = True
    while running:
        running = screen_manager.update()
        screen_manager.draw()
    pygame.quit()
if __name__ == "__main__":
    # DONT REMOVE IT
    with open("algorithm/new_des.txt", "w") as f:
        pass
    # ==================== 
    # _map = Map("test_case/level4/test2.txt")
    # level = Level3(_map)
    # print(level.run())
    # level = Level3(_map)
    # print(level.run())
    # new_path = convert_tuples_to_strings(path)
    # print(new_path)
    main()






# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     game_screen = GameScreen(screen, 'input.txt', path)

#     running = True
#     while running:
#         running = game_screen.update()
#         game_screen.draw()

#     pygame.quit()

# if __name__ == "__main__":
#     main()









# if __name__ == "__main__":

#     screen = GameScreen('input.txt', path)
#     screen.execute()
