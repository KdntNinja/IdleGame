import pygame
import json


class GameSettings:
    def __init__(self, config_file="settings.json"):
        with open(config_file, "r") as f:
            self.config = json.load(f)

        self.width = (
            self.config.get("game_settings", {}).get("resolution", {}).get("width", 800)
        )
        self.height = (
            self.config.get("game_settings", {})
            .get("resolution", {})
            .get("height", 600)
        )
        self.fullscreen = self.config.get("game_settings", {}).get("fullscreen", False)
        self.background_color = tuple(
            self.config.get("game_settings", {}).get("background_color", [0, 0, 0])
        )
        self.font = self.config.get("game_settings", {}).get("font", "Arial")
        self.exit_key = self.config.get("exit_key", pygame.K_ESCAPE)

    def get_display_flags(self):
        return pygame.FULLSCREEN if self.fullscreen else 0
