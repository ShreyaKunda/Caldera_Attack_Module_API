from src.utils import load_config
from src.caldera_client import CalderaClient
from src.attack_engine import AttackEngine
from src.mapping_builder import build_mapping

cfg = load_config()
client = CalderaClient(cfg["caldera_url"], cfg["api_key"], verify_ssl=cfg.get("verify_ssl", False))

if not client.authenticate():
    print("Auth failed. Check config/settings.json")
    exit(1)

# ensure mapping exists
import pathlib
if not pathlib.Path("config/ability_mapping.json").exists():
    print("Building mapping from data/abilities.xlsx ...")
    build_mapping()

engine = AttackEngine(client)
tactics = engine.list_tactics()
print("Tactics available:", tactics[:10])
# pick first tactic / first technique
if tactics:
    tactic = tactics[0]
    techniques = engine.list_techniques(tactic)
    if techniques:
        technique = techniques[0]
        ability = engine.select_ability(tactic, technique)
        agent = engine.pick_agent()
        if ability and agent:
            print(f"Executing ability {ability} on agent {agent['paw']}")
            res = engine.execute(ability, agent["paw"], mode=cfg.get("default_execution_mode", "direct"))
            print("Result:", res)
        else:
            print("No ability or no agent found.")
