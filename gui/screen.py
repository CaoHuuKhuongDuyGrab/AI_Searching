import pygame
from .components.map_view import MapView
from .components.sidebar import Sidebar
from test_case.read import *
from ultils import extend_paths
import abc
from .components.button import Text, Button
from .command import Command_StartGame, Command_BackMenu, Command_ChoosingMap
BUTTON_BACK = './gui/assets/back2.png'


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SIDEBAR_WIDTH = 300
SIDEBAR_HEIGHT = 600

NAVY_BLUE = (16, 44, 82)
WIDTH_BUTTON = 345
HEIGHT_BUTTON = 50
VSPACE = 80
SPACE = 180

MAP_WIDTH = 900
MAP_HEIGHT = 600

NAVY_BLUE = (16, 44, 82)
YELLOW = (230, 207, 108)
PLAY_EVENT = pygame.USEREVENT + 1

path = [
    "(1, 1) (2, 1) (3, 1) (4, 1) (5, 1) (6, 1) (6, 2) (6, 3) (5, 3) (5, 4) (5, 5) (6, 5) (7, 5) (7, 6) (7, 7) (7, 8)",
    "(1, 2) (1, 3) (1, 4) (1, 5) (2, 5)",
    "(1, 3) (1, 4) (1, 5)",
    "(1, 4) (1, 5) (1, 6)",
    "(1, 5) (1, 6) (1, 7)"
        ]





class ScreenManager:
    def __init__(self, screen):
        self.menu_screen = MenuScreen(screen,self)
        self.game_screen = GameScreen(screen, self.menu_screen.current_input_files, path, self)
        self.choosingmap_screen = ChoosingMapScreen(screen, self)
        self.current_screen = self.menu_screen
    def set_screen(self, new_screen):
        self.screen = new_screen
    def update(self):
        return self.current_screen.update()
    def draw(self):
        self.current_screen.draw()



class Screen(abc.ABC):
    def __init__(self, screen):
        self.screen = screen

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

class MenuScreen(Screen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.text_GameOver = Text(SCREEN_WIDTH / 2 ,100, "agent searching",font_size=66, color=(255,255,255))
        self.button_Start = Button(SCREEN_WIDTH / 2 - SPACE, 190, WIDTH_BUTTON, HEIGHT_BUTTON, 'start', command=Command_StartGame(screen_manager))
        self.button_ChooseMap = Button(SCREEN_WIDTH / 2 -SPACE, 190 + VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'choose map', command=Command_ChoosingMap(screen_manager)) 
        self.button_Credit = Button(SCREEN_WIDTH / 2 -SPACE, 190 + 2*VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'credit', command=None) 
        self.button_Exit = Button(SCREEN_WIDTH / 2 -SPACE, 190 + 3*VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'exit', command=None) 
        self.input_files = ['input.txt', 'input1.txt', 'input2.txt', 'input3.txt','input4.txt']
        path =[ [
        "(1, 1) (2, 1) (3, 1) (4, 1) (5, 1) (6, 1) (6, 2) (6, 3) (5, 3) (5, 4) (5, 5) (6, 5) (7, 5) (7, 6) (7, 7) (7, 8)",
        "(1, 2) (1, 3) (1, 4) (1, 5) (2, 5)",
        "(1, 3) (1, 4) (1, 5)",
        "(1, 4) (1, 5) (1, 6)",
        "(1, 5) (1, 6) (1, 7)"
            ]
        ]
        map_choosen = 0
        self.current_input_files = self.input_files[map_choosen]
        self.current_path = path[map_choosen]
        self.background_image = pygame.image.load('valorax.jpeg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def update(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in [self.button_Start, self.button_ChooseMap, self.button_Credit, self.button_Exit]:
                if button.is_clicked(event):
                    if button == self.button_Exit:
                        running = False
                        break
                    button.command.execute()
        return running

    def draw(self):
        # self.screen.fill(NAVY_BLUE) 
        self.screen.blit(self.background_image, (0, 0))
        self.text_GameOver.draw(self.screen)           
        self.button_Start.draw(self.screen)
        self.button_ChooseMap.draw(self.screen)
        self.button_Credit.draw(self.screen)
        self.button_Exit.draw(self.screen)
        pygame.display.flip()





class GameScreen(Screen):
    def __init__(self, screen, input_map, solution_path, screen_manager):
        super().__init__(screen)
        self.n, self.m, self.t, self.f, self.map_data, self.number_agents = read_input(input_map)
        self.paths = extend_paths(solution_path)
        self.map_view = MapView(self.screen, SIDEBAR_WIDTH, 0, MAP_WIDTH, MAP_HEIGHT, self.map_data, self.number_agents, solution_path=self.paths)
        self.sidebar = Sidebar(SIDEBAR_WIDTH, SIDEBAR_HEIGHT, self.map_view, screen_manager)

    def update(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == PLAY_EVENT:
                self.sidebar.next_step()
            self.sidebar.handle_event(event)
        return running
    def draw(self):
        self.sidebar.draw(self.screen)
        self.map_view.draw_map()
        pygame.display.flip()




class ChoosingMapScreen(Screen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.button_BackMenu = Button(40, 50 , WIDTH_BUTTON, HEIGHT_BUTTON, 'BACK', command=Command_BackMenu(screen_manager), isCircle= True, image_path= BUTTON_BACK) 
    def update(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if self.button_BackMenu.is_clicked(event):
                self.button_BackMenu.command.execute()
        return running
    def draw(self):
        self.screen.fill(NAVY_BLUE) 
        self.button_BackMenu.draw(self.screen)
        pygame.display.flip()

