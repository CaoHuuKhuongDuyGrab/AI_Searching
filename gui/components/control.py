import pygame

class Controls:
    def __init__(self):
        self.zoom_level = 1.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.zoom_in()
            elif event.key == pygame.K_MINUS:
                self.zoom_out()

    def zoom_in(self):
        self.zoom_level *= 1.1
        print("Zoom In:", self.zoom_level)

    def zoom_out(self):
        self.zoom_level /= 1.1
        print("Zoom Out:", self.zoom_level)
