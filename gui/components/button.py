import pygame

COLOUR_BUTTON = (230, 207, 108)
COLOUR_TEXT_BLACK = (0,0,0)


class Button:
    def __init__(self, x, y, width, height, text, image_path = None, color= COLOUR_BUTTON, text_color= COLOUR_TEXT_BLACK, isCircle = False):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)
        self.isCircle = isCircle
        self.radius = min(width, height) // 2 if isCircle else 0
        self.image = pygame.image.load(image_path) if image_path else None
        if self.image and isCircle:
            self.image = pygame.transform.scale(self.image, (self.radius, self.radius))


    def draw(self, screen):
        if not self.isCircle:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=200)
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
            image_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, image_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.isCircle:
                distance = ((event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y) ** 2) ** 0.5
                if distance <= self.radius:
                    return True
            else:
                if self.rect.collidepoint(event.pos):
                    return True
        return False
    def update_text(self, new_text):
        self.text = new_text