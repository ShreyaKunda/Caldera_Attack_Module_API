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

    def authenticate(self):
        """Validate API key by hitting a known endpoint."""
        try:
            logger.info("Testing Caldera API key authentication...")
            r = self.session.get(f"{self.server_url}/api/v2/adversaries", verify=self.verify_ssl)
            if r.status_code == 200:
                logger.info("✅ API key authentication successful")
                return True
            logger.error(f"❌ API key authentication failed: {r.status_code} {r.text}")
            return False
        except requests.RequestException as e:
            logger.error(f"❌ Authentication error: {e}")
            return False

    def get_agents(self):
        r = self.session.get(f"{self.server_url}/api/v2/agents", verify=self.verify_ssl)
        return r.json() if r.status_code == 200 else []

    def get_adversaries(self):
        r = self.session.get(f"{self.server_url}/api/v2/adversaries", verify=self.verify_ssl)
        return r.json() if r.status_code == 200 else []

    def get_abilities(self):
        r = self.session.get(f"{self.server_url}/api/v2/abilities", verify=self.verify_ssl)
        return r.json() if r.status_code == 200 else []

    def get_planners(self):
        r = self.session.get(f"{self.server_url}/api/v2/planners", verify=self.verify_ssl)
        if r.status_code == 200:
            return r.json()
        logger.error(f"❌ Failed to retrieve planners: {r.status_code} {r.text}")
        return []

    # ===============================================================
    # 🔥 NEW: Group abilities by MITRE ATT&CK technique
    # ===============================================================
    def get_techniques_with_abilities(self):
        """
        Returns a dict mapping MITRE techniques to a list of ability metadata.
        """
        abilities = self.get_abilities()
        technique_map = {}

        for ab in abilities:
            tech_id = ab.get("technique_id", "UNKNOWN")
            tech_name = ab.get("technique_name", "Unknown Technique")
            key = f"{tech_id} - {tech_name}"

            if key not in technique_map:
                technique_map[key] = []

            technique_map[key].append({
                "ability_id": ab.get("ability_id"),
                "name": ab.get("name"),
                "description": ab.get("description")
            })

        return technique_map

    # ===============================================================
    # 🔥 Execute a single ability
    # ===============================================================
    def execute_single_ability(self, ability_id, agent_id, use_direct=False):
        """
        Execute a single ability on a specific agent.
        """
        if use_direct:
            url = f"{self.server_url}/api/v2/agents/{agent_id}/execute"
            payload = {"ability_id": ability_id}
            logger.info(f"⚡ Running ability {ability_id} directly on agent {agent_id}")
            r = self.session.post(url, json=payload, verify=self.verify_ssl)

            if r.status_code in (200, 201):
                return {"success": True, "mode": "direct", "response": r.json()}
            return {"success": False, "error": f"{r.status_code}: {r.text}"}

        logger.info(f"🚀 Creating operation to run ability {ability_id} on agent {agent_id}")

        operation_payload = {
            "name": f"SingleAbility-{ability_id}",
            "state": "running",
            "autonomous": 1,
            "agents": [agent_id],
            "abilities": [ability_id]
        }

        r = self.session.post(f"{self.server_url}/api/v2/operations", json=operation_payload, verify=self.verify_ssl)

        if r.status_code in (200, 201):
            return {"success": True, "mode": "operation", "operation": r.json()}
        return {"success": False, "error": f"{r.status_code}: {r.text}"}

    # ===============================================================
    # 🔥 Execute by Technique (Auto ability selection)
    # ===============================================================
    def execute_by_technique(self, technique_name_or_id, agent_id, auto_select=True):
        """
        Find and execute abilities matching a MITRE technique.
        """
        techniques = self.get_techniques_with_abilities()

        matching = {k: v for k, v in techniques.items() if technique_name_or_id.lower() in k.lower()}

        if not matching:
            return {"success": False, "error": "Technique not found"}

        tech_key = list(matching.keys())[0]
        abilities = matching[tech_key]

        if auto_select:
            ability_id = abilities[0]["ability_id"]
            return self.execute_single_ability(ability_id, agent_id)

        return {
            "success": True,
            "technique": tech_key,
            "abilities": abilities
        }

    # ===============================================================
    # Existing full attack execution (unchanged)
    # ===============================================================
    def execute_attack_scenario(self, scenario_name, adversary_id, planner_id, agent_group="red", timeout=300):
        payload = {
            "name": scenario_name,
            "adversary": {"adversary_id": adversary_id},
            "planner": {"id": planner_id},
            "state": "running",
            "autonomous": 1,
            "host_group": agent_group
        }

        r = self.session.post(f"{self.server_url}/api/v2/operations", json=payload, verify=self.verify_ssl)
        if r.status_code in (200, 201):
            return {"success": True, "operation": r.json()}
        return {"success": False, "error": f"{r.status_code}: {r.text}"}
