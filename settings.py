import pygame
import json


class GameSettings:
    def __init__(self, config_file="settings.json"):
        pygame.init()

        with open(config_file, "r") as f:
            self.config = json.load(f)

        if self.config.get("game_settings", {}).get("fullscreen", False):
            self.width, self.height = (
                pygame.display.Info().current_w,
                pygame.display.Info().current_h,
            )
        else:
            self.width = (
                self.config.get("game_settings", {})
                .get("resolution", {})
                .get("width", 800)
            )
            self.height = (
                self.config.get("game_settings", {})
                .get("resolution", {})
                .get("height", 600)
            )

        # Scale `default_point_speed` to a percentage of 1–100%
        default_speed = self.config.get("game_settings", {}).get("default_point_speed", 1)
        self.default_point_speed = max(1, min(default_speed, 100))  # Clamp between 1 and 100
        self.speed_multiplier = self.default_point_speed / 100.0  # Convert to 0.01–1.0 multiplier

        self.fullscreen = self.config.get("game_settings", {}).get("fullscreen", False)
        self.background_color = tuple(
            self.config.get("game_settings", {}).get("background_color", [0, 0, 0])
        )
        self.font = (
                self.config.get("game_settings", {}).get("font")
                or pygame.font.get_default_font()
        )
        self.font_path = self.config.get("game_settings", {}).get("font_path")
        self.exit_key = self.config.get("exit_key", pygame.K_ESCAPE)

    def get_display_flags(self):
        return pygame.FULLSCREEN if self.fullscreen else 0
