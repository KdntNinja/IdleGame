import json


class GameState:
    speed_upgrade_cost = None
    speed_upgrade_value = None

    def __init__(self, save_file="save.json"):
        self.save_file = save_file
        try:
            with open(save_file, "r") as f:
                state = json.load(f)
                self.score = state.get("score", 0)
                self.speed_upgrade_cost = state.get("speed_upgrade_cost", 20)
                self.speed_upgrade_value = state.get("speed_upgrade_value", 1)
                self.passive_income = state.get(
                    "passive_income", {"passive_income": 0, "upgrade_cost": 10}
                )
                self.click_power = state.get(
                    "click_power", {"value": 1, "upgrade_cost": 10}
                )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Log issues when reading the save file and set default values
            print(f"[Error] Failed to load save file '{save_file}': {e}")
            self.speed_upgrade_cost = 20
            self.speed_upgrade_value = 1
            self.score = 0
            self.passive_income = {"passive_income": 0, "upgrade_cost": 10}
            self.click_power = {"value": 1, "upgrade_cost": 10}

        # Initialize passive income accumulator
        self.passive_income_accumulator = 0

    def save_game_state(self):
        state = {
            "score": self.score,
            "passive_income": self.passive_income,
            "click_power": self.click_power,
            "speed_upgrade_cost": self.speed_upgrade_cost,
            "speed_upgrade_value": self.speed_upgrade_value,
        }
        try:
            with open(self.save_file, "w") as f:
                json.dump(state, f, indent=4)
        except Exception as e:
            print(f"[Error] Failed to save game state to {self.save_file}: {e}")

    def increment_speed_upgrade_value(self, increment=1):
        """ Increment the speed upgrade value and save the state. """
        self.speed_upgrade_value += increment
        self.save_game_state()
