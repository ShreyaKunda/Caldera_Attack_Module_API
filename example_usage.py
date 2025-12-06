import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from caldera_attack_module import CalderaAttack

SERVER_URL = "http://192.168.195.128:8888"
API_KEY = "ADMIN123"
VERIFY_SSL = False

def interactive_mode():
    print("🎮 Interactive Caldera Attack Mode")
    print("=" * 40)

    caldera = CalderaAttack(SERVER_URL, API_KEY, VERIFY_SSL)

    if not caldera.authenticate():
        print("❌ Authentication failed. Exiting.")
        return

    while True:
        print("\nSelect an operation:")
        print("1. List agents")
        print("2. List adversaries")
        print("3. List abilities")
        print("4. Execute single ability")
        print("5. Run full attack scenario")
        print("6. List techniques")
        print("7. Execute attack by MITRE technique")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            agents = caldera.get_agents()
            print(f"\n📱 Agents ({len(agents)}):")
            for agent in agents:
                print(f"  - {agent.get('paw')}: {agent.get('host')}")

        elif choice == "2":
            adversaries = caldera.get_adversaries()
            print(f"\n🎭 Adversaries ({len(adversaries)}):")
            for i, adv in enumerate(adversaries, start=1):
                print(f"{i}. {adv.get('name')} - {adv.get('description')}")

        elif choice == "3":
            abilities = caldera.get_abilities()
            print(f"\n⚡ Abilities ({len(abilities)}):")
            for ability in abilities[:10]:
                print(f"  - {ability.get('name')} ({ability.get('ability_id')})")
            if len(abilities) > 10:
                print(f"... and {len(abilities) - 10} more")

        elif choice == "4":
            abilities = caldera.get_abilities()
            for i, ab in enumerate(abilities[:30], start=1):
                print(f"{i}. {ab.get('name')} ({ab.get('ability_id')})")

            ab_choice = int(input("Select ability number: ").strip())
            agent = caldera.get_agents()[0]["paw"]

            ability_id = abilities[ab_choice - 1]["ability_id"]
            result = caldera.execute_single_ability(ability_id, agent)
            print("Result:", result)

        elif choice == "5":
            adversaries = caldera.get_adversaries()
            planners = caldera.get_planners()
            result = caldera.execute_attack_scenario(
                "InteractiveAttack",
                adversaries[0]["adversary_id"],
                planners[0]["id"]
            )
            print(result)

        elif choice == "6":
            techs = caldera.get_techniques_with_abilities()
            print("\n🎯 MITRE Techniques:")
            for tech, items in techs.items():
                print(f"- {tech} ({len(items)} abilities)")

        elif choice == "7":
            technique = input("Enter MITRE Technique ID or name (ex: T1059): ").strip()
            agent = caldera.get_agents()[0]["paw"]
            result = caldera.execute_by_technique(technique, agent)
            print(result)

        elif choice == "8":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid selection.")

if __name__ == "__main__":
    interactive_mode()
