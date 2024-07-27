import pygame
from collections import deque
from ultils import read_output


WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (34, 70, 120)


LIGHT_GREEN = (173, 255, 219, 0)
LIGHT_ORANGE = (255, 192, 153)
LIGHT_PURPLE = (198, 164, 252)
NAVY_GREEN = (102, 153, 0)
HEAVY_BROWN = (125, 26, 26)
GREY = (169, 169, 169)
PINK_PINK=  (175, 0, 196)
RED = (255, 0, 0)
BLUE_1 = (0, 0, 255)
GREEN = (0, 255, 0)

LIGHT_YELLOW = (243, 255, 184)
LIGHT_BLUE = (182, 225, 252)

NAVY_BLUE = (16, 44, 82)
BORDER_COLOR = (0, 0, 0)  
PINK = (252, 182, 214)
YELLOW = (230, 207, 108)
AGENTS_COLOUR = [LIGHT_GREEN, LIGHT_ORANGE, LIGHT_PURPLE, NAVY_GREEN, HEAVY_BROWN, GREY, PINK_PINK, RED, BLUE_1, GREEN]



class Agent:
    def __init__(self, colour, path, name=None):
        self.colour = colour
        self.path = None
        self.numberSteps = 0
        if(path == '-1' or path == None):
            self.path = '-1'
        else:
            self.path, self.numberSteps = read_output(path)
        self.name = name
        self.pathIndex = 0
        self.lines = deque()
class MapView:
    def __init__(self, screen, x, y, width, height, map_data, number_agents, solution_path, screen_manager):
        self.screen = screen
        self.screen_manager = screen_manager
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.map_data = map_data
        self.number_agents = number_agents
        self.grid_x = int(width / len(map_data[0]))
        self.grid_y = int(height / len(map_data))
        self.map_surface = pygame.Surface((width, height))
        self.colored_squares = {} 
        self.text_in_squares = {}  
        self.images_in_squares = {} 
        self.font = pygame.font.Font(None, 36)  
        self.agents = []
        self.solution_path = solution_path
        self.update_agents()
        # self.coord_agent_map = {}  # Track the most recent agent for each coordinate
        self.line_order = [] 

        # print(self.solution_path)
    def draw_map(self):
        self.map_surface.fill(WHITE)  
        for x in range(0, self.width, self.grid_x):
            pygame.draw.line(self.map_surface, BORDER_COLOR, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_y):
            pygame.draw.line(self.map_surface, BORDER_COLOR, (0, y), (self.width, y))
        for x in range (len(self.map_data)):
            for y in range (len(self.map_data[0])):
                if (self.map_data[x][y] == -1):
                    self.color_square(x, y, BLUE)
                elif (str(self.map_data[x][y]).startswith('S')):
                    for agent in self.agents:
                        if agent.name == self.map_data[x][y]:
                            # if self.screen_manager.choosinglevel_screen.currentLevel <= 3:
                            #     # if agent.name == 'S':
                            #     self.color_square(x, y, agent.colour, agent.name)
                            # else:
                            self.color_square(x, y, agent.colour, agent.name)
                elif (str(self.map_data[x][y]).startswith('G')):
                    if str(self.map_data[x][y]) == 'G':
                        self.color_square(x, y, AGENTS_COLOUR[0], str(self.map_data[x][y]))
                    else:
                        goal_name = str(self.map_data[x][y])
                        i = int(goal_name[1:])
                        self.color_square(x, y, AGENTS_COLOUR[i], str(self.map_data[x][y]))
                elif (str(self.map_data[x][y]).startswith('F')):
                    # if self.screen_manager.choosinglevel_screen.currentLevel >= 3:
                    self.color_square(x, y, LIGHT_YELLOW, str(self.map_data[x][y]))
                elif(self.map_data[x][y] > 0):
                    # if self.screen_manager.choosinglevel_screen.currentLevel >= 2:
                    self.color_square(x, y, LIGHT_BLUE, str(self.map_data[x][y]))

        for (x, y), color in self.colored_squares.items():
            rect = pygame.Rect(y * self.grid_x, x * self.grid_y, self.grid_x, self.grid_y)
            pygame.draw.rect(self.map_surface, color, rect)
            pygame.draw.rect(self.map_surface, BORDER_COLOR, rect, 1)

        for (x, y), (text, image_path) in self.images_in_squares.items():
            rect = pygame.Rect(y * self.grid_x, x * self.grid_y, self.grid_x, self.grid_y)
            if text:
                text_surf = self.font.render(text, True, BLACK)
                text_rect = text_surf.get_rect(center=rect.center)
                self.map_surface.blit(text_surf, text_rect)
            if image_path:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (self.grid_x -1, self.grid_y - 1))
                image_rect = image.get_rect(center=rect.center)
                self.map_surface.blit(image, image_rect)

#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================               
        # for agent in self.agents:
        #     if agent.path != None and agent.path != -1:
        #         for start, end in agent.lines:
        #             pygame.draw.line(self.map_surface, agent.colour, start, end, 4)


#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================

        # lines_to_draw = []
        # for agent in self.agents:
        #     if agent.path not in [None, '-1']:
        #         for i, (start, end) in enumerate(agent.lines):
        #             lines_to_draw.append((start, end, agent.colour, i))
        # lines_to_draw.sort(key=lambda x: x[3])

        # for start, end, colour, _ in lines_to_draw:
        #     pygame.draw.line(self.map_surface, colour, start, end,30)
#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================

        for (start, end, colour) in self.line_order:
            pygame.draw.line(self.map_surface, colour, start, end, 4)


        self.screen.blit(self.map_surface, (self.x, self.y))

    def color_square(self, grid_x, grid_y, color, text=None, image_path=None):
        self.colored_squares[(grid_x, grid_y)] = color
        self.images_in_squares[(grid_x, grid_y)] = (text, image_path)

    def draw_line(self, start_grid, end_grid, agent):
        start_pos = (start_grid[1] * self.grid_x + self.grid_x // 2, start_grid[0] * self.grid_y + self.grid_y // 2)
        end_pos = (end_grid[1] * self.grid_x + self.grid_x // 2, end_grid[0] * self.grid_y + self.grid_y // 2)
        agent.lines.append((start_pos, end_pos))
        agent.pathIndex += 1
#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================
        # self.coord_agent_map[start_grid] = agent
        # self.coord_agent_map[end_grid] = agent

#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================
        self.line_order.append((start_pos, end_pos, agent.colour))

    def remove_line(self, agent):
        # if agent.lines:
        #     agent.lines.pop()
        #     agent.pathIndex -= 1
        if agent.lines:
            last_line = agent.lines.pop()
            start_pos, end_pos = last_line
            agent.pathIndex -= 1

#========================================================================================================
#========================================================================================================
#========================================================================================================
#========================================================================================================
            # for coord in [start_pos, end_pos]:
            #     if self.coord_agent_map.get(coord) == agent:
            #         del self.coord_agent_map[coord]   
            self.line_order = [(start, end, colour) for (start, end, colour) in self.line_order if not (start == start_pos and end == end_pos)]
                    
    def update_agents(self):
        for x in range (len(self.map_data)):
            for y in range (len(self.map_data[0])):
                if str(self.map_data[x][y]).startswith('S'):
                    # print(str(self.map_data[x][y]))
                    agent_name = str(self.map_data[x][y])
                    if agent_name == 'S':
                        agent_index = 0
                    else:
                        agent_index = int(agent_name[1:])
                    if agent_index < len(self.solution_path):
                        agent = Agent(AGENTS_COLOUR[agent_index], self.solution_path[agent_index], agent_name)
                    else:
                        agent = Agent(AGENTS_COLOUR[agent_index], '-1', agent_name)
                    self.agents.append(agent)
