import json, random

class AttackEngine:
    def __init__(self, client, mapping_path="config/ability_mapping.json"):
        self.client = client
        with open(mapping_path) as f:
            self.mapping = json.load(f)

    def select_random_technique(self):
        tactic = random.choice(list(self.mapping.keys()))
        technique = random.choice(list(self.mapping[tactic].keys()))
        ability_id = random.choice(self.mapping[tactic][technique])
        return tactic, technique, ability_id

    def pick_agent(self, agents):
        return random.choice(agents)

    def execute_random_attack(self):
        agents = self.client.get_agents()
        tactic, technique, ability = self.select_random_technique()
        agent = self.pick_agent(agents)
        result = self.client.run_operation(agent, ability)

        return {
            "tactic": tactic,
            "technique": technique,
            "ability_id": ability,
            "agent": agent["paw"],
            "result": result
        }
