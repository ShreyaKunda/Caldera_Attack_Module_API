import json, random
from pathlib import Path
from .utils import load_mapping

class AttackEngine:
    def __init__(self, client, mapping_path="config/ability_mapping.json"):
        self.client = client
        self.mapping_path = mapping_path
        self.mapping = load_mapping(mapping_path)

    def reload_mapping(self):
        self.mapping = load_mapping(self.mapping_path)
        return self.mapping

    def list_tactics(self):
        return list(self.mapping.keys())

    def list_techniques(self, tactic):
        return list(self.mapping.get(tactic, {}).keys())

    def list_subtechniques(self, tactic, technique_label):
        tech = self.mapping.get(tactic, {}).get(technique_label)
        if not tech:
            return {}
        return tech.get("subtechniques", {})

    def select_ability(self, tactic, technique_label, sub_id=None):
        """
        Returns ability_id (first candidate) or None.
        If sub_id provided, tries that subtechnique list first.
        """
        tech = self.mapping.get(tactic, {}).get(technique_label)
        if not tech:
            return None

        if sub_id:
            subs = tech.get("subtechniques", {})
            abilities = subs.get(sub_id, [])
            return random.choice(abilities) if abilities else None

        default_list = tech.get("default", [])
        if default_list:
            return random.choice(default_list)
        # fallback — any subtechnique ability
        subs = tech.get("subtechniques", {})
        for lst in subs.values():
            if lst:
                return random.choice(lst)
        return None

    def pick_agent(self, explicit_paw=None):
        agents = self.client.get_agents()
        if not agents:
            return None
        if explicit_paw:
            for a in agents:
                if a.get("paw") == explicit_paw:
                    return a
            return None
        # pick first available by default
        return agents[0]

    def execute(self, ability_id, agent_paw, mode="direct"):
        """
        mode: "direct" or "operation"
        """
        if mode == "direct":
            return self.client.execute_direct(agent_paw, ability_id)
        else:
            name = f"Auto-Single-{ability_id}"
            return self.client.create_operation(name, [agent_paw], [ability_id])
