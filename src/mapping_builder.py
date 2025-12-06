import pandas as pd, json, os

def build_mapping():
    df = pd.read_excel("data/abilities.xlsx")
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]

    mapping = {}
    for _, row in df.iterrows():
        tactic = row["tactic"]
        tech_id = row["technique_id"]
        tech_name = row["technique_name"]
        ability_id = row["id"]

        label = f"{tech_id} - {tech_name}"

        mapping.setdefault(tactic, {})
        mapping[tactic].setdefault(label, [])
        mapping[tactic][label].append(ability_id)

    with open("config/ability_mapping.json", "w") as f:
        json.dump(mapping, f, indent=4)

    print("✅ Mapping generated successfully.")
