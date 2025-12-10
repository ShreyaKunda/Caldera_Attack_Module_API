import logging
import requests

logger = logging.getLogger("caldera_attack_module")
logging.basicConfig(level=logging.INFO)

class CalderaAttack:
    def __init__(self, server_url, api_key, verify_ssl=False):
        self.server_url = server_url.rstrip("/")
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update({
            "KEY": self.api_key,
            "Content-Type": "application/json"
        })

    # ------------------------
    # Authentication
    # ------------------------
    def authenticate(self):
        try:
            logger.info("Testing Caldera API key authentication...")
            r = self.session.get(f"{self.server_url}/api/v2/adversaries",
                                 verify=self.verify_ssl)
            if r.status_code == 200:
                logger.info("✅ API key authentication successful")
                return True
            logger.error(f"❌ API key authentication failed: {r.status_code} {r.text}")
            return False
        except requests.RequestException as e:
            logger.error(f"❌ Authentication error: {e}")
            return False

    # ------------------------
    # Fetch resources
    # ------------------------
    def get_agents(self):
        r = self.session.get(f"{self.server_url}/api/v2/agents",
                             verify=self.verify_ssl)
        return r.json() if r.status_code == 200 else []

    def get_adversaries(self):
        r = self.session.get(f"{self.server_url}/api/v2/adversaries",
                             verify=self.verify_ssl)
        return r.json() if r.status_code == 200 else []

    def get_abilities(self):
        r = self.session.get(f"{self.server_url}/api/v2/abilities",
                             verify=self.verify_ssl)
        return r.json() if r.status_code == 200 else []

    def get_planners(self):
        r = self.session.get(f"{self.server_url}/api/v2/planners",
                             verify=self.verify_ssl)
        if r.status_code == 200:
            return r.json()
        logger.error(f"❌ Failed to retrieve planners: {r.status_code} {r.text}")
        return []

    # ------------------------
    # Technique Filtering
    # ------------------------
    def get_abilities_by_techniques(self, technique_ids):
        """
        Filters abilities based on MITRE technique IDs.
        technique_ids: list like ["T1059", "T1047"]
        """
        all_abilities = self.get_abilities()
        filtered = [
            ab for ab in all_abilities
            if ab.get("technique", {}).get("attack_id") in technique_ids
        ]
        return filtered

    # ------------------------
    # Create a custom adversary with selected abilities
    # ------------------------
    def create_custom_adversary(self, name, ability_ids):
        payload = {
            "name": name,
            "description": f"Custom adversary for {name}",
            "abilities": [{"ability_id": ab} for ab in ability_ids]
        }

        r = self.session.post(f"{self.server_url}/api/v2/adversaries",
                              json=payload, verify=self.verify_ssl)

        if r.status_code in (200, 201):
            return r.json()
        else:
            logger.error(f"❌ Failed to create adversary: {r.status_code} {r.text}")
            return None

    # ------------------------
    # Run attack using selected MITRE techniques
    # ------------------------
    def run_technique_attack(self, scenario_name, technique_ids,
                             planner_id, agent_group="red", timeout=300):

        abilities = self.get_abilities_by_techniques(technique_ids)
        if not abilities:
            return {"success": False,
                    "error": f"No abilities found for techniques: {technique_ids}"}

        ability_ids = [ab["ability_id"] for ab in abilities]

        # Create custom adversary
        adversary = self.create_custom_adversary(
            f"{scenario_name}_adversary",
            ability_ids
        )

        if adversary is None:
            return {"success": False,
                    "error": "Failed creating custom adversary"}

        adversary_id = adversary["adversary_id"]

        return self.execute_attack_scenario(
            scenario_name,
            adversary_id,
            planner_id,
            agent_group
        )

    # ------------------------
    # Execute scenario
    # ------------------------
    def execute_attack_scenario(self, scenario_name, adversary_id,
                                planner_id, agent_group="red", timeout=300):

        payload = {
            "name": scenario_name,
            "adversary": {"adversary_id": adversary_id},
            "planner": {"id": planner_id},
            "state": "running",
            "autonomous": 1,
            "host_group": agent_group
        }

        r = self.session.post(f"{self.server_url}/api/v2/operations",
                              json=payload, verify=self.verify_ssl)

        if r.status_code in (200, 201):
            return {"success": True, "operation": r.json()}
        else:
            return {"success": False,
                    "error": f"{r.status_code}: {r.text}"}
