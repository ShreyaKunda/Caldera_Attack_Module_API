import sys
import os

# Add src/ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from caldera_attack_module import CalderaAttack

SERVER_URL = "http://192.168.195.128:8888"   # Modify if needed
API_KEY = "ADMIN123"                         # Your API key (red/blue)
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
        print("4. Run attack scenario (normal)")
        print("5. Exit")
        print("6. Run attack by MITRE techniques")

        choice = input("\nEnter your choice (1-6): ").strip()

        # -------------------------------------------------------
        # 1. AGENTS
        # -------------------------------------------------------
        if choice == "1":
            agents = caldera.get_agents()
            print(f"\n📱 Agents ({len(agents)}):")
            for agent in agents:
                print(f"  - {agent.get('paw')}: {agent.get('host')}")

        # -------------------------------------------------------
        # 2. ADVERSARIES
        # -------------------------------------------------------
        elif choice == "2":
            adversaries = caldera.get_adversaries()
            print(f"\n🎭 Adversaries ({len(adversaries)}):")
            for i, adv in enumerate(adversaries, start=1):
                print(f"{i}. {adv.get('name')} - {adv.get('description')}")

        # -------------------------------------------------------
        # 3. ABILITIES
        # -------------------------------------------------------
        elif choice == "3":
            abilities = caldera.get_abilities()
            print(f"\n⚡ Abilities ({len(abilities)}):")
            for ability in abilities[:10]:
                print(f"  - {ability.get('name')}: {ability.get('description')}")
            if len(abilities) > 10:
                print(f"... and {len(abilities) - 10} more")

        # -------------------------------------------------------
        # 4. NORMAL SCENARIO
        # -------------------------------------------------------
        elif choice == "4":
            scenario_name = input("Enter a name for this operation: ").strip() or "Interactive_Op"

            adversaries = caldera.get_adversaries()
            print("\nAvailable adversaries:")
            for i, adv in enumerate(adversaries, start=1):
                print(f"{i}. {adv.get('name')} - {adv.get('description')}")

            adv_choice = int(input("Choose adversary #: ").strip())
            adversary_id = adversaries[adv_choice - 1].get("adversary_id")

            planners = caldera.get_planners()
            print("\nAvailable planners:")
            for i, p in enumerate(planners, start=1):
                print(f"{i}. {p.get('name')} - {p.get('description')}")

            plan_choice = int(input("Choose planner #: ").strip())
            planner_id = planners[plan_choice - 1].get("id")

            print(f"\n🚀 Running scenario '{scenario_name}'...")
            results = caldera.execute_attack_scenario(
                scenario_name,
                adversary_id,
                planner_id
            )

            if results["success"]:
                print("✅ Scenario completed successfully!")
            else:
                print(f"❌ Scenario failed: {results['error']}")

        # -------------------------------------------------------
        # 6. TECHNIQUE-BASED ATTACKS
        # -------------------------------------------------------
        elif choice == "6":
            print("\n👉 Enter MITRE techniques (comma separated, e.g. T1059,T1047):")
            techniques_input = input("Techniques: ").strip()
            technique_ids = [t.strip() for t in techniques_input.split(",")]

            planners = caldera.get_planners()
            print("\nAvailable planners:")
            for i, p in enumerate(planners, start=1):
                print(f"{i}. {p.get('name')} - {p.get('description')}")

            plan_choice = int(input("Choose planner #: ").strip())
            planner_id = planners[plan_choice - 1].get("id")

            print(f"\n🚀 Running technique-based attack with: {technique_ids}")
            result = caldera.run_technique_attack(
                "Technique_Based_Attack",
                technique_ids,
                planner_id
            )

            if result["success"]:
                print("✅ Technique attack executed!")
            else:
                print(f"❌ Error: {result['error']}")

        # -------------------------------------------------------
        # 5. EXIT
        # -------------------------------------------------------
        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter 1-6.")


def run_basic_attack_scenario():
    caldera = CalderaAttack(SERVER_URL, API_KEY, VERIFY_SSL)
    if not caldera.authenticate():
        print("❌ Authentication failed.")
        return False

    agents = caldera.get_agents()
    adversaries = caldera.get_adversaries()
    planners = caldera.get_planners()

    if not agents or not adversaries or not planners:
        print("❌ Missing required resources.")
        return False

    adversary_id = adversaries[0]["adversary_id"]
    batch_planner = next(
        (p for p in planners if p.get("name", "").lower() == "batch"),
        planners[0]
    )
    planner_id = batch_planner["id"]

    print(f"🚀 Running default scenario with adversary '{adversaries[0]['name']}'")
    results = caldera.execute_attack_scenario(
        "RL_Training_Attack_Scenario",
        adversary_id,
        planner_id
    )

    if results["success"]:
        print("✅ Basic scenario completed successfully!")
        return True
    else:
        print(f"❌ Scenario failed: {results['error']}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        run_basic_attack_scenario()
