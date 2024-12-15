import pygame
from settings import GameSettings
from state import GameState
from ui_manager import UIManager


class ClickerGame:
    def __init__(self):
        self.settings = GameSettings()
        self.state = GameState()

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height),
            self.settings.get_display_flags(),
        )
        pygame.display.set_caption("Simple Clicker Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.ui_manager = UIManager(self.settings, self.state, self.screen)

        self.click_button_rect = pygame.Rect(
            self.settings.width // 2 - 50, self.settings.height // 2 - 25, 100, 50
        )
        self.upgrade_click_rect = pygame.Rect(
            self.settings.width // 2 - 100, self.settings.height - 170, 200, 50
        )
        self.upgrade_income_rect = pygame.Rect(
            self.settings.width // 2 - 100, self.settings.height - 100, 200, 50
        )

        self.click_button_colors = ((100, 149, 237), (70, 130, 180))  # Blue shades
        self.upgrade_click_colors = ((34, 139, 34), (50, 205, 50))  # Green shades
        self.upgrade_income_colors = ((255, 140, 0), (255, 165, 0))  # Orange shades

        self.mouse_clicked = False

    def apply_passive_income(self):
        self.state.passive_income_accumulator += (
            self.state.passive_income["income_per_second"] / 60
        )
        while self.state.passive_income_accumulator >= 1:
            self.state.score += 1
            self.state.passive_income_accumulator -= 1

    def handle_events(self):
        self.mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == self.settings.exit_key
            ):
                self.running = False
                self.state.save_game_state()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_clicked = True

    def game_loop(self):
        while self.running:
            self.handle_events()
            self.apply_passive_income()

            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(self.settings.background_color)

            self.ui_manager.draw_button(
                self.click_button_rect,
                "Click",
                mouse_pos,
                self.mouse_clicked,
                self.on_click,
                *self.click_button_colors,
            )
            self.ui_manager.draw_button(
                self.upgrade_click_rect,
                f"Upgrade Click ({self.state.click_power['upgrade_cost']})",
                mouse_pos,
                self.mouse_clicked,
                self.upgrade_click_power,
                *self.upgrade_click_colors,
            )
            self.ui_manager.draw_button(
                self.upgrade_income_rect,
                f"Upgrade Income ({self.state.passive_income['upgrade_cost']})",
                mouse_pos,
                self.mouse_clicked,
                self.upgrade_income,
                *self.upgrade_income_colors,
            )
            self.ui_manager.render()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def on_click(self):
        self.state.score += self.state.click_power["value"]

    def upgrade_click_power(self):
        if self.state.score >= self.state.click_power["upgrade_cost"]:
            self.state.score -= self.state.click_power["upgrade_cost"]
            self.state.click_power["value"] += 1
            self.state.click_power["upgrade_cost"] = int(
                self.state.click_power["upgrade_cost"] * 1.5
            )

    def upgrade_income(self):
        if self.state.score >= self.state.passive_income["upgrade_cost"]:
            self.state.score -= self.state.passive_income["upgrade_cost"]
            self.state.passive_income["income_per_second"] += 1
            self.state.passive_income["upgrade_cost"] = int(
                self.state.passive_income["upgrade_cost"] * 1.5
            )


if __name__ == "__main__":
    game = ClickerGame()
    game.game_loop()
