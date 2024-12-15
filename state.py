import json


class GameState:
    def __init__(self, save_file="save.json"):
        self.save_file = save_file
        try:
            with open(save_file, "r") as f:
                state = json.load(f)
                self.score = state.get("score", 0)
                self.passive_income = state.get(
                    "passive_income", {"income_per_second": 0, "upgrade_cost": 10}
                )
                self.click_power = state.get(
                    "click_power", {"value": 1, "upgrade_cost": 10}
                )
        except (FileNotFoundError, json.JSONDecodeError):
            self.score = 0
            self.passive_income = {"income_per_second": 0, "upgrade_cost": 10}
            self.click_power = {"value": 1, "upgrade_cost": 10}

        self.passive_income_accumulator = 0

    def save_game_state(self):
        state = {
            "score": self.score,
            "passive_income": self.passive_income,
            "click_power": self.click_power,
        }
        with open(self.save_file, "w") as f:
            json.dump(state, f)
