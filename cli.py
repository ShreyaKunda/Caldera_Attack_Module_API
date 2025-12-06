import json
from src.caldera_client import CalderaClient
from src.attack_engine import AttackEngine
from src.mapping_builder import build_mapping
from src.utils import log_info, log_success, log_error

def main():
    settings = json.load(open("config/settings.json"))

    # Create mapping if missing
    try:
        open("config/ability_mapping.json")
    except:
        log_info("Mapping file missing. Building from CSV...")
        build_mapping("data/abilities.csv", "config/ability_mapping.json")

    client = CalderaClient(settings["caldera_url"], settings["api_key"])
    engine = AttackEngine(client, "config/ability_mapping.json")

    agents = client.get_agents()
    if not agents:
        log_error("No active agents found.")
        return

    agent_id = agents[0]['paw']
    log_success(f"Selected agent: {agent_id}")

    techniques = engine.list_techniques()

    print("\nAvailable MITRE Techniques:")
    for i, t in enumerate(techniques):
        print(f"[{i}] {t}")

    try:
        choice = int(input("\nSelect technique number: "))
    except:
        log_error("Invalid selection.")
        return

    technique = techniques[choice]
    log_info(f"Selected Technique: {technique}")

    engine.run_attack(technique, agent_id)


if __name__ == "__main__":
    main()
