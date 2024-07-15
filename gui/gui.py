import pygame
from components import MapView, Controls

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Map Application")

    map_view = MapView(screen, 800, 600)
    controls = Controls()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            controls.handle_event(event)

        screen.fill((255, 255, 255))  # Fill the screen with white color
        map_view.draw_map()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
