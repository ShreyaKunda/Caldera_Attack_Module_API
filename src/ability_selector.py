import json

class AbilitySelector:
    def __init__(self, caldera_instance, technique_map_path="technique_map.json"):
        self.caldera = caldera_instance
        self.abilities = self.caldera.get_abilities()
        self.technique_map = json.load(open(technique_map_path))

    def list_technique_categories(self):
        return list(self.technique_map.keys())

    def list_matching_abilities(self, category):
        category = category.lower()
        if category not in self.technique_map:
            return []

        technique_ids = self.technique_map[category]
        return [a for a in self.abilities if a.get("technique_id") in technique_ids]

    def select_by_index(self, category, index):
        abilities = self.list_matching_abilities(category)
        if not abilities:
            return None
        return abilities[index] if index < len(abilities) else None
