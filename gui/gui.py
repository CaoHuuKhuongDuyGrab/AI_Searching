import pygame
from .components.map_view import MapView
from .components.sidebar import Sidebar
from test_case.read import *


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SIDEBAR_WIDTH = 300
SIDEBAR_HEIGHT = 600

MAP_WIDTH = 900
MAP_HEIGHT = 600


YELLOW = (230, 207, 108)
PLAY_EVENT = pygame.USEREVENT + 1

def extend_paths(paths):
    parsed_paths = [list(map(lambda s: tuple(map(int, s.strip('()').split(','))), path.split(') ('))) for path in paths]
    max_length = max(len(path) for path in parsed_paths)
    extended_paths = []
    for path in parsed_paths:
        if len(path) < max_length:
            last_coord = path[-1]
            path.extend([last_coord] * (max_length - len(path)))
        extended_paths.append(path)
    extended_paths_str = [' '.join(f'({x},{y})' for (x, y) in path) for path in extended_paths]
    return extended_paths_str

class GUI:
    def __init__(self, input_map, solution_path):
        self.n, self.m, self.t, self.f, self.map_data, self.number_agents = read_input(input_map)
        self.screen = None
        self.map_view = None
        self.sidebar = None
        self.paths = extend_paths(solution_path)
    def execute(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Agent Searching")
        self.map_view = MapView(self.screen, SIDEBAR_WIDTH, 0, MAP_WIDTH, MAP_HEIGHT, self.map_data, self.number_agents, solution_path= self.paths)
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

