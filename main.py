import json
import pygame


class App:
    def __init__(self, config_file="settings.json", save_file="save.json"):
        # Load configuration and save files
        self.config_file = config_file
        self.save_file = save_file
        self.settings = self.load_json_file(config_file, default={})
        self.game_state = self.load_json_file(
            save_file,
            default={
                "score": 0,
                "passive_income": {"income_per_second": 0, "upgrade_cost": 10},
                "click_power": {"value": 1, "upgrade_cost": 20},
            },
        )

        # Initialize Pygame
        pygame.init()

        # Game settings
        self.apply_loaded_settings()

        # Application state
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = self.game_state.get("score", 0)
        self.passive_income = self.game_state.get("passive_income", {"income_per_second": 0, "upgrade_cost": 10})
        self.click_power = self.game_state.get("click_power", {"value": 1, "upgrade_cost": 20})
        self.passive_income_accumulator = 0  # For fractional income tracking

    def load_json_file(self, file_path, default):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    def apply_loaded_settings(self):
        # Extract and apply settings to the game
        game_settings = self.settings.get("game_settings", {})
        self.resolution = game_settings.get("resolution", {"width": 800, "height": 600})
        self.width = self.resolution.get("width")
        self.height = self.resolution.get("height")
        self.fullscreen = game_settings.get("fullscreen", False)
        self.flags = pygame.FULLSCREEN if self.fullscreen else 0
        pygame.display.set_caption(self.settings.get("title", "Simple Clicker Game"))
        self.screen = pygame.display.set_mode((self.width, self.height), self.flags)
        self.background_color = tuple(game_settings.get("background_color", [0, 0, 0]))
        self.button_color = tuple(game_settings.get("button_color", [255, 0, 0]))
        self.button_hover_color = tuple(game_settings.get("button_hover_color", [200, 0, 0]))
        self.button_rect = pygame.Rect(self.width // 2 - 50, self.height // 2 - 25, 100, 50)

    def display_text(self, message, size, position=(10, 10), color=(255, 255, 255)):
        font = pygame.font.SysFont(self.settings.get("game_settings", {}).get("font", "Arial"), size)
        text = font.render(message, True, color)
        self.screen.blit(text, position)

    def show_fps(self):
        fps = round(self.clock.get_fps(), 2)
        self.display_text(str(fps), 15, position=(10, 10), color=self.button_color)

    def draw_button(self, text):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.button_rect.collidepoint(mouse_pos) and mouse_click[0] and not getattr(self, "mouse_clicked", False):
            self.score += self.click_power["value"]
            self.mouse_clicked = True
            if self.score % 10 == 0:  # Autosave every 10 clicks
                self.save_game()
        if not mouse_click[0]:
            self.mouse_clicked = False

        button_color = self.button_hover_color if self.button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, button_color, self.button_rect)

        font = pygame.font.SysFont(self.settings.get("game_settings", {}).get("font", "Arial"), 20)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_upgrade_click_power_button(self):
        button_rect = pygame.Rect(self.width // 2 - 100, self.height - 170, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            if self.score >= self.click_power["upgrade_cost"]:
                self.score -= self.click_power["upgrade_cost"]
                self.click_power["value"] += 1
                self.click_power["upgrade_cost"] = int(self.click_power["upgrade_cost"] * 1.5)
                self.save_game()  # Autosave on upgrade

        button_color = (100, 100, 0) if not button_rect.collidepoint(mouse_pos) else (150, 150, 0)
        pygame.draw.rect(self.screen, button_color, button_rect)

        font = pygame.font.SysFont(self.settings.get("game_settings", {}).get("font", "Arial"), 20)
        text_surface = font.render(
            f"Upgrade Click ({self.click_power['upgrade_cost']})", True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_passive_income_button(self):
        button_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            if self.score >= self.passive_income["upgrade_cost"]:
                self.score -= self.passive_income["upgrade_cost"]
                self.passive_income["income_per_second"] += 1
                self.passive_income["upgrade_cost"] = int(self.passive_income["upgrade_cost"] * 1.5)
                self.save_game()  # Autosave on upgrade

        button_color = (0, 100, 0) if not button_rect.collidepoint(mouse_pos) else (0, 150, 0)
        pygame.draw.rect(self.screen, button_color, button_rect)

        font = pygame.font.SysFont(self.settings.get("game_settings", {}).get("font", "Arial"), 20)
        text_surface = font.render(
            f"Upgrade Income ({self.passive_income['upgrade_cost']})", True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def apply_passive_income(self):
        self.passive_income_accumulator += self.passive_income["income_per_second"] / 60
        while self.passive_income_accumulator >= 1:
            self.score += 1
            self.passive_income_accumulator -= 1

    def save_game(self):
        self.game_state = {
            "score": self.score,
            "passive_income": self.passive_income,
            "click_power": self.click_power,
        }
        with open(self.save_file, "w") as f:
            json.dump(self.game_state, f)

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == self.settings.get("exit_key", pygame.K_ESCAPE)
                ):
                    self.running = False
                    self.save_game()  # Autosave on quit

            self.screen.fill(self.background_color)

            self.apply_passive_income()
            self.show_fps()
            self.draw_button("Click")
            self.draw_passive_income_button()
            self.draw_upgrade_click_power_button()
            self.display_text(f"Score: {int(self.score)}", 30, position=(self.width // 2 - 50, 10), color=(255, 255, 255))
            self.display_text(f"Click Power: {self.click_power['value']}", 20, position=(10, 40), color=(255, 255, 255))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.game_loop()
