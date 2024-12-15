import pygame


class UIManager:
    def __init__(self, settings, state, screen):
        self.settings = settings
        self.state = state
        self.screen = screen
        self.font = pygame.font.SysFont(self.settings.font, 20)

    def draw_text(self, text, size, position, color=(255, 255, 255)):
        font = pygame.font.SysFont(self.settings.font, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_button(self, rect, text, mouse_pos, clicked, on_click, color, hover_color):
        button_color = hover_color if rect.collidepoint(mouse_pos) else color
        pygame.draw.rect(self.screen, button_color, rect)

        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

        if rect.collidepoint(mouse_pos) and clicked:
            on_click()

    def render(self):
        self.draw_text(f"Score: {int(self.state.score)}", 30, (10, 10))
        self.draw_text(f"Click Power: {self.state.click_power['value']}", 20, (10, 40))
