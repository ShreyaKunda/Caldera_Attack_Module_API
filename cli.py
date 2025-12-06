import json
from src.caldera_client import CalderaClient
from src.attack_engine import AttackEngine

def main():
    config = json.load(open("config/settings.json"))
    client = CalderaClient(config)

    if not client.authenticate():
        print("❌ Authentication failed. Check API key or URL.")
        return

    engine = AttackEngine(client)
    result = engine.execute_random_attack()

    print("\n🔥 ATTACK EXECUTED 🔥")
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
