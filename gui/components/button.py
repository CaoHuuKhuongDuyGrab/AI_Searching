import pygame

COLOUR_BUTTON = (230, 207, 108)
COLOUR_TEXT_BLACK = (0,0,0)


class Button:
    def __init__(self, x, y, width, height, text, command, image_path = None, color= COLOUR_BUTTON, text_color= COLOUR_TEXT_BLACK, isCircle = False, font = "valorax.otf"):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(font, 36)
        self.isCircle = isCircle
        self.radius = min(width, height) // 2 if isCircle else 0
        self.image = pygame.image.load(image_path) if image_path else None
        if self.image and isCircle:
            self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        self.command = command
        self.highlighted = False  # New attribute to manage highlight state
    def draw(self, screen):
        if not self.isCircle:
            if self.highlighted:
                pygame.draw.rect(screen, (255,255,255), self.rect, border_radius=1000)
            else:
                pygame.draw.rect(screen, self.color, self.rect, border_radius=1000)
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
    def set_highlight(self, highlighted):
        self.highlighted = highlighted


class Text:
    def __init__(self, x, y, text, font_size = 36, font_path = "valorax.otf", color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(font_path, font_size)
        self.text_surface = self.font.render(text, True, color)
        self.rect = self.text_surface.get_rect(center=(x, y))

    def draw(self, screen):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect(center=(self.x, self.y))
        screen.blit(self.text_surface, self.rect)