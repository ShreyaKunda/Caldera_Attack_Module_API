#!/usr/bin/env python3
import json
from src.utils import load_config
from src.caldera_client import CalderaClient
from src.attack_engine import AttackEngine
from src.mapping_builder import build_mapping
from pathlib import Path

def main():
    # 1. load config
    cfg = load_config()
    client = CalderaClient(cfg["caldera_url"], cfg["api_key"], verify_ssl=cfg.get("verify_ssl", False))

    if not client.authenticate():
        print("❌ Could not authenticate to Caldera. Check config/settings.json (URL and API key).")
        return

    # 2. ensure mapping exists - if not, try build (if data/abilities.xlsx present)
    mapping_file = Path("config/ability_mapping.json")
    if not mapping_file.exists():
        print("⚠ ability_mapping.json not found. Attempting to build from data/abilities.xlsx ...")
        try:
            build_mapping()
        except Exception as e:
            print("❌ Failed to build mapping automatically:", e)
            return

    engine = AttackEngine(client)

    while True:
        print("\n=== Caldera Attack CLI ===")
        print("1) List tactics")
        print("2) List techniques for a tactic")
        print("3) Execute technique (choose)")
        print("4) Execute random technique on first agent")
        print("5) Rebuild mapping from data/abilities.xlsx")
        print("6) Exit")
        choice = input("Choose (1-6): ").strip()
        if choice == "1":
            t = engine.list_tactics()
            for i, x in enumerate(t, start=1):
                print(f"{i}. {x}")
        elif choice == "2":
            tactic = input("Enter tactic name (case sensitive, copy from list): ").strip()
            if tactic not in engine.mapping:
                print("Tactic not found.")
                continue
            techs = engine.list_techniques(tactic)
            for i, tt in enumerate(techs, start=1):
                print(f"{i}. {tt}")
        elif choice == "3":
            tactic = input("Enter tactic name: ").strip()
            tech = input("Enter technique label (copy exactly): ").strip()
            subs = engine.list_subtechniques(tactic, tech)
            if subs:
                print("Subtechniques found:")
                for i, s in enumerate(subs.keys(), start=1):
                    print(f"{i}. {s}")
                use_sub = input("Use subtechnique? (enter id or leave blank): ").strip() or None
            else:
                use_sub = None
            ability = engine.select_ability(tactic, tech, sub_id=use_sub)
            if not ability:
                print("No ability mapped to this selection.")
                continue
            agent_paw = engine.pick_agent().get("paw")
            mode = input("Execution mode (direct/operation) [default from config]: ").strip() or cfg.get("default_execution_mode", "direct")
            print(f"Executing ability {ability} on agent {agent_paw} (mode={mode}) ...")
            res = engine.execute(ability, agent_paw, mode=mode)
            print("Result:", res)
        elif choice == "4":
            tactic,technique,ability = engine.select_random_choice() if hasattr(engine, "select_random_choice") else (None,None,None)
            # we don't have select_random_choice by default; do random selection manually:
            import random
            tactics = engine.list_tactics()
            if not tactics:
                print("No tactics loaded.")
                continue
            t = random.choice(tactics)
            techs = engine.list_techniques(t)
            tech = random.choice(techs)
            ability = engine.select_ability(t, tech)
            agent_paw = engine.pick_agent().get("paw")
            mode = cfg.get("default_execution_mode", "direct")
            print(f"Random execute: {t} -> {tech} -> ability {ability} on {agent_paw}")
            res = engine.execute(ability, agent_paw, mode=mode)
            print("Result:", res)
        elif choice == "5":
            try:
                build_mapping()
            except Exception as e:
                print("Build failed:", e)
        elif choice == "6":
            print("Bye.")
            break
        else:
            print("Unknown choice.")

if __name__ == "__main__":
    main()
