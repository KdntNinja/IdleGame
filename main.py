import json

import pygame


class App:
    def __init__(self, config_file="settings.json"):
        with open(config_file, "r") as f:
            settings = json.load(f)
        pygame.init()

        game_settings = settings.get("game_settings", {})
        resolution = game_settings.get("resolution", {})
        width = resolution.get("width", 800)
        height = resolution.get("height", 600)
        fullscreen = game_settings.get("fullscreen", False)

        flags = pygame.FULLSCREEN if fullscreen else 0

        pygame.display.set_caption(settings.get("title", "Simple Pygame App"))
        self.screen = pygame.display.set_mode((width, height), flags)
        self.background_color = tuple(game_settings.get("background_color", [0, 0, 0]))
        self.running = True

        # Access other settings like audio, controls, etc., if needed
        self.audio_settings = game_settings.get("audio", {})
        self.controls = game_settings.get("controls", {})
        self.player_profile = settings.get("player_profile", {})
        self.save_slots = settings.get("save_slots", [])

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(self.background_color)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.game_loop()
