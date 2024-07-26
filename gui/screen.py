import abc
import pygame
import pygame_widgets
from pygame_widgets.dropdown import Dropdown

from test_case.read import *
from .components.map_view import MapView
from .components.sidebar import Sidebar
from .components.button import Text, Button
from ultils import parse_path, generate_inputfile_path
from .command import Command_StartGame, Command_BackMenu, Command_EnterMap, Command_EnterCreditScreen, Command_BackChoosingMap, Command_StartChoosingAlgorithm, Command_ChoosingLevel

BUTTON_BACK = './gui/assets/back2.png'



SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SIDEBAR_WIDTH = 300
SIDEBAR_HEIGHT = 600
WHITE = (255,255,255)
NAVY_BLUE = (16, 44, 82)
WIDTH_BUTTON = 380
HEIGHT_BUTTON = 50
VSPACE = 80
HSPACE = 60
SPACE = 180

MAP_WIDTH = 900
MAP_HEIGHT = 600

NAVY_BLUE = (16, 44, 82)
YELLOW = (230, 207, 108)
PLAY_EVENT = pygame.USEREVENT + 1



class ScreenManager:
    def __init__(self, screen):
        self.menu_screen = MenuScreen(screen,self)
        self.choosinglevel_screen = ChoosingLevelScreen(screen, self)
        self.choosingmap_screen = ChoosingMapScreen(screen, self)
        self.choosingalgorithm_screen = ChoosingAlgorithmScreen(screen, self)
        self.credit_screen = CreditScreen(screen, self)
        self.game_screen = GameScreen(screen, self)
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
        self.text_AgentSearching = Text(SCREEN_WIDTH / 2 ,100, "agent searching",font_size=66, color=(255,255,255))
        self.button_Start = Button(SCREEN_WIDTH / 2 - SPACE, 190, WIDTH_BUTTON, HEIGHT_BUTTON, 'start', command=Command_EnterMap(screen_manager))
        self.button_Chooselevel = Button(SCREEN_WIDTH / 2 -SPACE, 190 + VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'choose level', command=Command_ChoosingLevel(screen_manager)) 
        self.button_Credit = Button(SCREEN_WIDTH / 2 -SPACE, 190 + 2*VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'credit', command=Command_EnterCreditScreen(screen_manager)) 
        self.button_Exit = Button(SCREEN_WIDTH / 2 -SPACE, 190 + 3*VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'exit', command=None) 
        # self.input_files = ['input.txt', 'input1.txt', 'input2.txt', 'input3.txt','input4.txt']
        # map_choosen = 0
        # self.current_input_files = self.input_files[map_choosen]
        # self.current_path = path[map_choosen]
        self.background_image = pygame.image.load('valorax.jpeg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def update(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in [self.button_Start, self.button_Chooselevel, self.button_Credit, self.button_Exit]:
                if button.is_clicked(event):
                    if button == self.button_Exit:
                        running = False
                        break
                    button.command.execute()
        return running

    def draw(self):
        # self.screen.fill(NAVY_BLUE) 
        self.screen.blit(self.background_image, (0, 0))
        self.text_AgentSearching.draw(self.screen)           
        self.button_Start.draw(self.screen)
        self.button_Chooselevel.draw(self.screen)
        self.button_Credit.draw(self.screen)
        self.button_Exit.draw(self.screen)
        pygame.display.flip()


class GameScreen(Screen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.is_level1 = True
        self.input_map = generate_inputfile_path(self.screen_manager.choosinglevel_screen.currentLevel, self.screen_manager.choosingmap_screen.currentMap)      
        if self.screen_manager.choosingmap_screen.input_map:
            self.n, self.m, self.t, self.f, self.map_data, self.number_agents = read_input(self.screen_manager.choosingmap_screen.input_map, self.screen_manager.choosinglevel_screen.currentLevel)
            self.paths = parse_path(self.input_map, self.screen_manager.choosinglevel_screen.currentLevel, self.screen_manager.choosingalgorithm_screen.currentAlgorithm)
            # print(self.paths)
            self.map_view = MapView(self.screen, SIDEBAR_WIDTH, 0, MAP_WIDTH, MAP_HEIGHT, self.map_data, self.number_agents, solution_path=self.paths, screen_manager=self.screen_manager)
            # self.map_view = MapView(self.screen, SIDEBAR_WIDTH, 0, MAP_WIDTH, MAP_HEIGHT, self.map_data, self.number_agents, solution_path=self.paths)
            self.sidebar = Sidebar(SIDEBAR_WIDTH, SIDEBAR_HEIGHT, self.map_view, self.screen_manager, self.t, self.f)
    def update(self):
        # input_map = generate_inputfile_path(self.screen_manager.choosinglevel_screen.currentLevel, self.screen_manager.choosingmap_screen.currentMap)
        # print(input_map)
        # self.n, self.m, self.t, self.f, self.map_data, self.number_agents = read_input(input_map)
        # self.paths = extend_paths(path)
        # self.map_view = MapView(self.screen, SIDEBAR_WIDTH, 0, MAP_WIDTH, MAP_HEIGHT, self.map_data, self.number_agents, solution_path=self.paths)
        # self.sidebar = Sidebar(SIDEBAR_WIDTH, SIDEBAR_HEIGHT, self.map_view, self.screen_manager)
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == PLAY_EVENT:
                self.sidebar.next_step()
            self.sidebar.handle_event(event)
        return running
    def draw(self):
        if self.sidebar:
            self.sidebar.draw(self.screen)
        if self.map_view:
            self.map_view.draw_map()
        pygame.display.flip()


class ChoosingLevelScreen(Screen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.button_BackMenu = Button(40, 50 , WIDTH_BUTTON, HEIGHT_BUTTON, 'BACK', command=Command_BackMenu(screen_manager), isCircle= True, image_path= BUTTON_BACK) 
        self.font = pygame.font.Font('valorax.otf', 32)  # Adjust as needed
        self.currentLevel = 1
        self.dropdown = Dropdown(screen, SCREEN_WIDTH / 2 - 200, 140, 360, 50, name='choose a level',
    choices=[
        'Level 1',
        'Level 2',
        'Level 3',
        'Level 4'
    ],
    borderRadius=3, colour=pygame.Color(YELLOW), values=[1, 2, 3, 4], direction='down', textHAlign='left', font=self.font, hoverColour= WHITE, pressedColour = WHITE
)
        self.background_image = pygame.image.load('valorax.jpeg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def update(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in [self.button_BackMenu]:
                if button.is_clicked(event):
                    button.command.execute()
                    if self.dropdown.getSelected() != None:
                        self.currentLevel = self.dropdown.getSelected()  
            pygame_widgets.update(event)
            pygame.display.update()
        return running
    def draw(self):
        # self.screen.fill(NAVY_BLUE)
        self.screen.blit(self.background_image, (0, 0))
        self.button_BackMenu.draw(self.screen)
        self.dropdown.draw()
        pygame.display.flip()



class ChoosingMapScreen(Screen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.currentMap = 1
        self.input_map = generate_inputfile_path(self.screen_manager.choosinglevel_screen.currentLevel, 1)
        self.button_BackMenu = Button(40, 50 , 240, 50, 'BACK', command=Command_BackMenu(screen_manager), isCircle= True, image_path= BUTTON_BACK)
        self.button_OK = None
        self.button_Map1 = Button(190, 150 , 240, 50, 'MAP 1', command=None) 
        self.button_Map2 = Button(490, 150 , 240, 50, 'MAP 2', command=None) 
        self.button_Map3 = Button(790, 150 , 240, 50, 'MAP 3', command=None) 
        self.button_Map4 = Button(331, 250 , 240, 50, 'MAP 4', command=None) 
        self.button_Map5 = Button(639, 250 , 240, 50, 'MAP 5', command=None) 
        self.font = pygame.font.Font('valorax.otf', 32) 
        self.background_image = pygame.image.load('valorax.jpeg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def update(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            buttons =  [self.button_BackMenu, self.button_Map1, self.button_Map2, self.button_Map3, self.button_Map4, self.button_Map5, self.button_OK]
            for index, button in enumerate(buttons):
                if button != None and button.is_clicked(event):
                    if button in [self.button_Map1, self.button_Map2, self.button_Map3, self.button_Map4, self.button_Map5]:
                        if self.screen_manager.choosinglevel_screen.currentLevel == 1:
                            self.button_OK = Button(540, SCREEN_HEIGHT - 150 , 130, 50, 'ok', command=Command_StartChoosingAlgorithm(self.screen_manager))
                        else:
                            self.button_OK = Button(540, SCREEN_HEIGHT - 150 , 130, 50, 'ok', command=Command_StartGame(self.screen_manager))
                        self.set_highlighted_button(button)
                        self.currentMap = index
                    if button == self.button_BackMenu:
                        self.button_OK = None
                        self.set_unhighlighted_button()
                    if  button.command:
                        if button == self.button_OK:
                            self.input_map = generate_inputfile_path(self.screen_manager.choosinglevel_screen.currentLevel, self.screen_manager.choosingmap_screen.currentMap)
                            n, m, t, f, map_data, number_agents = read_input(self.input_map, self.screen_manager.choosinglevel_screen.currentLevel)
                            paths = parse_path(self.input_map, self.screen_manager.choosinglevel_screen.currentLevel, self.screen_manager.choosingalgorithm_screen.currentAlgorithm)
                            self.screen_manager.game_screen.map_view = MapView(self.screen, SIDEBAR_WIDTH, 0, MAP_WIDTH, MAP_HEIGHT, map_data, number_agents, solution_path=paths, screen_manager=self.screen_manager)
                            self.screen_manager.game_screen.sidebar = Sidebar(SIDEBAR_WIDTH, SIDEBAR_HEIGHT, self.screen_manager.game_screen.map_view, self.screen_manager, t, f)
                        button.command.execute()
        return running
    
    def set_unhighlighted_button(self):
        for button in [self.button_Map1, self.button_Map2, self.button_Map3, self.button_Map4, self.button_Map5]:
            button.set_highlight(False)
    def set_highlighted_button(self, selected_button):
        self.set_unhighlighted_button()
        selected_button.set_highlight(True)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.button_BackMenu.draw(self.screen)
        self.button_Map1.draw(self.screen)
        self.button_Map2.draw(self.screen)
        self.button_Map3.draw(self.screen)
        self.button_Map4.draw(self.screen)
        self.button_Map5.draw(self.screen)
        if self.button_OK:
            self.button_OK.draw(self.screen)
        pygame.display.flip()


class CreditScreen(Screen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.button_BackMenu = Button(40, 50 , 240, 50, 'BACK', command=Command_BackMenu(screen_manager), isCircle= True, image_path= BUTTON_BACK)

        self.text_groupmember = Text(600,50, "group member",font_size=50, color=WHITE)

        self.text_name1_1 = Text(228,180, "22127011",font_size=50, color=WHITE)
        self.text_name1_2 = Text(650 ,180, "ha tuan anh",font_size=50, color=WHITE)

        self.text_name2_1 = Text(248,180 + 110, "22127083",font_size=50, color=WHITE)
        self.text_name2_2 = Text(790 ,180 + 110, "cao huu khuong duy",font_size=50, color=WHITE)

        self.text_name3_1 = Text(248 ,180 + 2*110, "22127383",font_size=50, color=WHITE)
        self.text_name3_2 = Text(758,180 + 2*110, "nguyen thanh thai",font_size=50, color=WHITE)

        self.text_name4_1 = Text(238,180 + 3*110, "22127414",font_size=50, color=WHITE)
        self.text_name4_2 = Text(626,180 + 3*110, "tu chi tien",font_size=50, color=WHITE)

        self.background_image = pygame.image.load('valorax.jpeg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def update(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in [self.button_BackMenu]:
                if button.is_clicked(event):
                    button.command.execute()
        return running    
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.button_BackMenu.draw(self.screen)

        self.text_groupmember.draw(self.screen)

        self.text_name1_1.draw(self.screen)
        self.text_name1_2.draw(self.screen)

        self.text_name2_1.draw(self.screen)
        self.text_name2_2.draw(self.screen)

        self.text_name3_1.draw(self.screen)
        self.text_name3_2.draw(self.screen)

        self.text_name4_1.draw(self.screen)
        self.text_name4_2.draw(self.screen)

        pygame.display.flip()



class ChoosingAlgorithmScreen(Screen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen)
        self.screen_manager = screen_manager
        self.currentAlgorithm = 1
        self.button_BackChoosingMap = Button(40, 50 , 240, 50, 'BACK', command=Command_BackChoosingMap(screen_manager), isCircle= True, image_path= BUTTON_BACK)
        self.button_OK = None
        self.button_BFS = Button(190, 150 , 240, 50, 'BFS', command=None) 
        self.button_DFS = Button(490, 150 , 240, 50, 'DFS', command=None) 
        self.button_UCS = Button(790, 150 , 240, 50, 'UCS', command=None) 
        self.button_GBFS = Button(331, 250 , 240, 50, 'GBFS', command=None) 
        self.button_ASTAR = Button(639, 250 , 240, 50, 'A-STAR', command=None) 
        self.font = pygame.font.Font('valorax.otf', 32) 
        self.background_image = pygame.image.load('valorax.jpeg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    def update(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            buttons =  [self.button_BackChoosingMap, self.button_BFS, self.button_DFS, self.button_UCS, self.button_GBFS, self.button_ASTAR, self.button_OK]
            for index, button in enumerate(buttons):
                if button != None and button.is_clicked(event):
                    if button in [self.button_BFS, self.button_DFS, self.button_UCS, self.button_GBFS, self.button_ASTAR]:
                        self.button_OK = Button(540, SCREEN_HEIGHT - 150 , 130, 50, 'ok', command=Command_StartGame(self.screen_manager))
                        self.set_highlighted_button(button)
                        self.currentAlgorithm = index
                    if button == self.button_BackChoosingMap:
                        self.button_OK = None
                        self.set_unhighlighted_button()
                    if  button.command:
                        self.screen_manager.game_screen = GameScreen(self.screen, self.screen_manager)
                        button.command.execute()
        return running
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.button_BFS.draw(self.screen)
        self.button_DFS.draw(self.screen)
        self.button_UCS.draw(self.screen)
        self.button_GBFS.draw(self.screen)
        self.button_ASTAR.draw(self.screen)
        self.button_BackChoosingMap.draw(self.screen)
        if self.button_OK:
            self.button_OK.draw(self.screen)
        pygame.display.flip()
    def set_unhighlighted_button(self):
        for button in [self.button_BFS, self.button_DFS, self.button_UCS, self.button_GBFS, self.button_ASTAR]:
            button.set_highlight(False)
    def set_highlighted_button(self, selected_button):
        self.set_unhighlighted_button()
        selected_button.set_highlight(True)