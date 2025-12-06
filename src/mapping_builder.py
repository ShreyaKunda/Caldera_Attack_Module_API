import pandas as pd
import json
from src.utils import log_success, log_error

def build_mapping(csv_path, output_json):
    try:
        df = pd.read_csv(csv_path)

        mapping = {}

        for _, row in df.iterrows():
            technique = str(row['technique_id']).strip()
            entry = {
                "id": row['id'],
                "name": row['name'],
                "plugin": row['plugin'],
                "tactic": row['tactic'],
                "description": row['description'],
                "subtechnique": row.get("subtechnique", "")
            }

            if technique not in mapping:
                mapping[technique] = []

            mapping[technique].append(entry)

        with open(output_json, "w") as f:
            json.dump(mapping, f, indent=4)

        log_success(f"Mapping file generated: {output_json}")

    except Exception as e:
        log_error(f"Mapping build failed: {e}")
