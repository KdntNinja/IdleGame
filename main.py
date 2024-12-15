import json

import pygame


class App:
    def __init__(self, config_file="settings.json"):
        # Load configuration file
        with open(config_file, "r") as f:
            self.settings = json.load(f)

        # Initialize Pygame
        pygame.init()

        # Game settings
        self.game_settings = self.settings.get("game_settings", {})
        self.resolution = self.game_settings.get(
            "resolution", {"width": 800, "height": 600}
        )
        self.width = self.resolution.get("width")
        self.height = self.resolution.get("height")
        self.fullscreen = self.game_settings.get("fullscreen", False)

        # Screen setup
        self.flags = pygame.FULLSCREEN if self.fullscreen else 0
        pygame.display.set_caption(self.settings.get("title", "Simple Clicker Game"))
        self.screen = pygame.display.set_mode((self.width, self.height), self.flags)
        self.background_color = tuple(
            self.game_settings.get("background_color", [0, 0, 0])
        )

        # Application state
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0

        # Button settings
        self.button_clicked = None
        self.button_color = tuple(self.game_settings.get("button_color", [255, 0, 0]))
        self.button_hover_color = tuple(
            self.game_settings.get("button_hover_color", [200, 0, 0])
        )
        self.button_rect = pygame.Rect(
            self.width // 2 - 50, self.height // 2 - 25, 100, 50
        )
        self.mouse_clicked = False

    def display_text(self, message, size, position=(10, 10), color=(255, 255, 255)):
        font = pygame.font.SysFont(self.game_settings.get("font", "Arial"), size)
        text = font.render(message, True, color)
        self.screen.blit(text, position)

    def show_fps(self):
        fps = round(self.clock.get_fps(), 2)
        self.display_text(str(fps), 15, position=(10, 10), color=self.button_color)

    def draw_button(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.button_rect.collidepoint(mouse_pos) and mouse_click[0] and not self.mouse_clicked:
            self.score += 1
            self.mouse_clicked = True

        if not mouse_click[0]:
            self.mouse_clicked = False

        button_color = self.button_hover_color if self.button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, button_color, self.button_rect)

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.background_color)
            self.show_fps()
            self.draw_button()
            self.display_text(f"Score: {self.score}", 30, position=(self.width // 2 - 50, 10), color=(255, 255, 255))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.game_loop()
