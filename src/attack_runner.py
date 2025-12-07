from .caldera_client import CalderaClient
from .ability_loader import AbilityLoader

class AttackRunner:
    def __init__(self, settings, csv_path):
        self.client = CalderaClient(
            settings["server_url"],
            settings["api_key"],
            settings["verify_ssl"]
        )
        self.loader = AbilityLoader(csv_path)

    def run_ability(self, ability):
        return self.client.execute_ability(ability["id"])
