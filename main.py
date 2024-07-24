from level.level_3 import Level3
from level.level_1 import Level1

from object.map import Map
from gui import GameScreen, ScreenManager, MenuScreen
import pygame


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SIDEBAR_WIDTH = 300
SIDEBAR_HEIGHT = 600

MAP_WIDTH = 900
MAP_HEIGHT = 600

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

    # _map = Map("test_case/input_lv3.txt")
    # print(_map.get_sources())
    # level = Level1(_map)
    # level.run()
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
