import json
import random
from src.utils import log_success, log_error

class AttackEngine:
    def __init__(self, client, mapping_file):
        self.client = client
        self.mapping = json.load(open(mapping_file))

    def list_techniques(self):
        return list(self.mapping.keys())

    def run_attack(self, technique_id, agent_id):
        if technique_id not in self.mapping:
            log_error("Technique not found in mapping.")
            return False

        selected = random.choice(self.mapping[technique_id])
        log_success(f"Executing ability: {selected['name']} ({selected['id']})")

        ok, response = self.client.execute_ability(agent_id, selected['id'])
        if ok:
            log_success("Execution successful!")
        return ok
