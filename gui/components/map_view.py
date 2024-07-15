import pygame

class MapView:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.map_surface = pygame.Surface((width, height))

    def draw_map(self):
        # Example: Draw a simple grid representing the map
        self.map_surface.fill((255, 255, 255))  # Fill with white color
        for x in range(0, self.width, 40):
            pygame.draw.line(self.map_surface, (0, 0, 0), (x, 0), (x, self.height))
        for y in range(0, self.height, 40):
            pygame.draw.line(self.map_surface, (0, 0, 0), (0, y), (self.width, y))
        self.screen.blit(self.map_surface, (0, 0))
