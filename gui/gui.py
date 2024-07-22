import pygame
from .components.map_view import MapView
from .components.sidebar import Sidebar

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SIDEBAR_WIDTH = 300
SIDEBAR_HEIGHT = 600

MAP_WIDTH = 900
MAP_HEIGHT = 600


YELLOW = (230, 207, 108)
PLAY_EVENT = pygame.USEREVENT + 1



def read_input(file_name):
    with open(file_name, 'r') as file:
        # Read the first line
        first_line = file.readline().strip()
        n, m, t, f = map(int, first_line.split())

        # Read the next n lines for the map
        map_data = []
        for _ in range(n):
            line = file.readline().strip().split()
            map_row = []
            for cell in line:
                if cell.startswith('F') or cell.startswith('S') or cell.startswith('G') or cell == -1:
                    map_row.append(cell)
                else:
                    map_row.append(int(cell))
            map_data.append(map_row)
    return map_data



class GUI:
    def __init__(self, input_map, solution_path):
        self.map_data = read_input(input_map)
        self.screen = None
        self.map_view = None
        self.sidebar = None
        self.paths = solution_path
    def execute(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Agent Searching")
        self.map_view = MapView(self.screen, SIDEBAR_WIDTH, 0, MAP_WIDTH, MAP_HEIGHT, self.map_data, solution_path= self.paths)
        self.sidebar = Sidebar(SIDEBAR_WIDTH, SIDEBAR_HEIGHT, self.map_view)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == PLAY_EVENT:
                    self.sidebar.next_step()
                self.sidebar.handle_event(event)
            self.sidebar.draw(self.screen)
            self.map_view.draw_map()
            pygame.display.flip()
        pygame.quit()

