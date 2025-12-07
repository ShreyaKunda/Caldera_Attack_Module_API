import json
from src.attack_runner import AttackRunner

SETTINGS = "config/settings.json"
CSV = "data/abilities.csv"

with open(SETTINGS) as f:
    settings = json.load(f)

runner = AttackRunner(settings, CSV)
ability = runner.loader.load()[0]  # first ability

print("\nRunning:", ability["name"])
print(runner.run_ability(ability))
