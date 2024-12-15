import pygame


class UIManager:
    def __init__(self, settings, state, screen):
        self.settings = settings
        self.state = state
        self.screen = screen
        self.font = pygame.font.Font(self.settings.font_path, 20)
        self.shadow_color = (30, 30, 30)
        self.shadow_offset = (2, 2)

    def draw_text(
            self, text, size, position, color=(255, 255, 255), outline_color=None, shadow=False
    ):
        font = pygame.font.Font(self.settings.font_path, size)
        if shadow:
            shadow_surface = font.render(text, True, self.shadow_color)
            shadow_position = (position[0] + self.shadow_offset[0], position[1] + self.shadow_offset[1])
            self.screen.blit(shadow_surface, shadow_position)
        text_surface = font.render(text, True, color)
        if outline_color:
            outline_surface = font.render(text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=position)
            self.screen.blit(outline_surface, outline_rect)
        self.screen.blit(text_surface, position)

    def draw_button(
            self, rect, text, mouse_pos, clicked, on_click, color, hover_color,
            round_radius=0, scale_hover_effect=1.1, tooltip=None, rounded=True, hover_effect=True
    ):
        button_color = hover_color if rect.collidepoint(mouse_pos) else color
        if hover_effect and rect.collidepoint(mouse_pos):
            rect = pygame.Rect(
                rect.left - int((rect.width * (scale_hover_effect - 1)) // 2),
                rect.top - int((rect.height * (scale_hover_effect - 1)) // 2),
                int(rect.width * scale_hover_effect),
                int(rect.height * scale_hover_effect),
            )
        if rounded:
            pygame.draw.rect(self.screen, button_color, rect, border_radius=round_radius)
        else:
            pygame.draw.rect(self.screen, button_color, rect)

        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

        if rect.collidepoint(mouse_pos) and clicked:
            on_click()

        if tooltip and rect.collidepoint(mouse_pos):
            tooltip_font = pygame.font.Font(self.settings.font_path, 16)
            tooltip_surface = tooltip_font.render(tooltip, True, (255, 255, 255))
            tooltip_pos = (mouse_pos[0] + 10, mouse_pos[1] - 20)
            pygame.draw.rect(
                self.screen, (0, 0, 0),
                (tooltip_pos[0] - 2, tooltip_pos[1] - 2, tooltip_surface.get_width() + 4,
                 tooltip_surface.get_height() + 4)
            )
            self.screen.blit(tooltip_surface, tooltip_pos)

    def draw_gradient_background(self):
        for y in range(self.settings.height):
            pygame.draw.line(
                self.screen,
                (0, 0, 50 + (y // 10)),
                (0, y),
                (self.settings.width, y),
            )

    def draw_progress_bar(self, position, size, progress, color=(0, 255, 0), outline_color=(255, 255, 255)):
        pygame.draw.rect(self.screen, outline_color, (*position, *size))
        inner_position = (position[0] + 2, position[1] + 2)
        inner_size = (size[0] - 4, size[1] - 4)
        pygame.draw.rect(self.screen, (128, 128, 128), (*inner_position, *inner_size))

        progress_size = (inner_size[0] * progress, inner_size[1])
        pygame.draw.rect(self.screen, color, (*inner_position, *progress_size))

    def draw_tooltip(self, color=(255, 255, 255)):
        self.draw_text(f"Score: {int(self.state.score)}", 30, (10, 10), color)
        self.draw_text(f"Click Power: {self.state.click_power['value']}", 20, (10, 40), color)

    def render(self):
        self.draw_tooltip()
