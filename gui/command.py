import pygame
PLAY_EVENT = pygame.USEREVENT + 1
PLAY_INTERVAL = 500



class Command:
    def execute(self):
        pass

class Command_Play(Command):
    def __init__(self, sidebar):
        self.sidebar = sidebar

    def execute(self):
        self.sidebar.is_playing = not self.sidebar.is_playing
        if self.sidebar.is_playing:
            print("Play started")
            pygame.time.set_timer(PLAY_EVENT, PLAY_INTERVAL)
            self.sidebar.button_Play.update_text("STOP")
        else:
            print("Play stopped")
            pygame.time.set_timer(PLAY_EVENT, 0)
            self.sidebar.button_Play.update_text("PLAY")

class Command_NextMove(Command):
    def __init__(self, sidebar):
        self.sidebar = sidebar
    def execute(self):
        # self.sidebar.next_move()
        self.sidebar.is_playing = False
        pygame.time.set_timer(PLAY_EVENT, 0)
        self.sidebar.button_Play.update_text("PLAY")
        self.sidebar.next_step()

class Command_PreviousMove(Command):
    def __init__(self, sidebar):
        self.sidebar = sidebar
    def execute(self):
        for agent in self.sidebar.map_view.agents:
            if agent.pathIndex > 0:
                self.sidebar.is_playing = False
                pygame.time.set_timer(PLAY_EVENT, 0)
                self.sidebar.button_Play.update_text("PLAY")
                self.sidebar.map_view.remove_line(agent)
        if self.sidebar.pathIndex > 0:
            self.sidebar.pathIndex -= 1



class Command_BackMenu(Command):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    def execute(self):
        self.screen_manager.current_screen = self.screen_manager.menu_screen
        print("Switched to Menu Screen")

class Command_BackChoosingMap(Command):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    def execute(self):
        self.screen_manager.current_screen = self.screen_manager.choosingmap_screen
        print("Switched to Choosing Screen")


class Command_BackChoosingAlgorithm(Command):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    def execute(self):
        self.screen_manager.current_screen = self.screen_manager.choosingalgorithm_screen
        print("Switched to Choosing Screen")



class Command_EnterMap(Command):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    def execute(self):
        self.screen_manager.current_screen = self.screen_manager.choosingmap_screen
        # print(self.screen_manager.choosinglevel_screen.currentLevel)


class Command_ChoosingLevel(Command):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    def execute(self):
        self.screen_manager.current_screen = self.screen_manager.choosinglevel_screen


class Command_StartGame(Command):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    def execute(self):
        self.screen_manager.current_screen = self.screen_manager.game_screen


class Command_StartChoosingAlgorithm(Command):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    def execute(self):
        self.screen_manager.current_screen = self.screen_manager.choosingalgorithm_screen

class Command_EnterCreditScreen(Command):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    def execute(self):
        self.screen_manager.current_screen = self.screen_manager.credit_screen