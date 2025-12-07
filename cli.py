import json
from src.attack_runner import AttackRunner

SETTINGS = "config/settings.json"
CSV = "data/abilities.csv"

with open(SETTINGS) as f:
    settings = json.load(f)

runner = AttackRunner(settings, CSV)
abilities = runner.loader.load()

print("\n=== Available Abilities ===")
for i, a in enumerate(abilities, start=1):
    print(f"{i}. {a['technique_id']} - {a['name']} ({a['tactic']})")

choice = int(input("\nEnter attack number: ")) - 1
selected = abilities[choice]

print(f"\n🚀 Executing: {selected['name']} ({selected['technique_id']})...")

result = runner.run_ability(selected)
print("\nResult:", result)
