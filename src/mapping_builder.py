"""
Reads data/abilities.xlsx and writes config/ability_mapping.json
Expected columns (case-insensitive):
- id
- plugin
- name
- description
- tactic
- technique_id
- technique_name
"""

import pandas as pd
import json
from pathlib import Path

INPUT = Path("data/abilities.xlsx")
OUTPUT = Path("config/ability_mapping.json")

def normalize_col(col):
    return col.strip().lower().replace(" ", "_")

def build_mapping(input_file=INPUT, output_file=OUTPUT):
    if not Path(input_file).exists():
        raise FileNotFoundError(f"abilities.xlsx not found at {input_file.resolve()}")

    df = pd.read_excel(input_file)
    df.columns = [normalize_col(c) for c in df.columns]

    required = {"id", "tactic", "technique_id", "technique_name"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in abilities.xlsx: {missing}")

    mapping = {}
    rows = df.to_dict(orient="records")
    for r in rows:
        tactic = str(r.get("tactic", "unknown")).strip()
        tech_id = str(r.get("technique_id", "")).strip()
        tech_name = str(r.get("technique_name", "")).strip()
        ability_id = str(r.get("id", "")).strip()

        if not tech_id:
            # place under 'unmapped'
            tech_id = "UNMAPPED"
            tech_name = "UNMAPPED"

        tactic_key = tactic or "unknown"
        mapping.setdefault(tactic_key, {})

        tech_label = f"{tech_id} - {tech_name}"

        # Create structure
        if tech_label not in mapping[tactic_key]:
            mapping[tactic_key][tech_label] = {"subtechniques": {}, "default": []}

        # If subtechnique (contains dot), e.g., T1059.001
        if "." in tech_id:
            base = tech_id.split(".")[0]
            # Store by full subtechnique id (Txxxx.xxx)
            mapping[tactic_key][tech_label]["subtechniques"].setdefault(tech_id, []).append(ability_id)
        else:
            mapping[tactic_key][tech_label]["default"].append(ability_id)

    # write out
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(mapping, f, indent=2)

    print(f"✅ Mapping written to {output_file.resolve()} (tactics: {len(mapping)})")
    return mapping

if __name__ == "__main__":
    build_mapping()
