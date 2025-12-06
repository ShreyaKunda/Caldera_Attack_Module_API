import logging
import requests
import yaml
import time

logger = logging.getLogger("caldera_attack_module")
logging.basicConfig(level=logging.INFO)

class CalderaAttack:
    def __init__(self, config_path="config.yml"):
        cfg = yaml.safe_load(open(config_path))

        self.server_url = cfg["server_url"].rstrip("/")
        self.api_key = cfg["api_key"]
        self.verify_ssl = cfg.get("verify_ssl", False)
        self.agent_group = cfg.get("default_agent_group", "red")

        self.session = requests.Session()
        self.session.headers.update({
            "KEY": self.api_key,
            "Content-Type": "application/json"
        })

        self.cached_abilities = None  # caching

    def authenticate(self):
        logger.info("Testing API Key authentication...")
        r = self.session.get(f"{self.server_url}/api/v2/agents", verify=self.verify_ssl)
        if r.status_code == 200:
            logger.info("✔ Authentication successful")
            return True
        logger.error(f"✘ Authentication failed: {r.text}")
        return False

    def get_agents(self):
        return self.session.get(f"{self.server_url}/api/v2/agents", verify=self.verify_ssl).json()

    def get_abilities(self):
        if self.cached_abilities:
            return self.cached_abilities
        r = self.session.get(f"{self.server_url}/api/v2/abilities", verify=self.verify_ssl)
        if r.status_code == 200:
            self.cached_abilities = r.json()
        return self.cached_abilities

    def execute_single_ability(self, ability_id, agent_group=None):
        if not agent_group:
            agent_group = self.agent_group

        payload = {
            "host_group": agent_group,
            "adversary": {
                "adversary_id": None
            },
            "phases": {
                "1": [ability_id]
            }
        }

        r = self.session.post(f"{self.server_url}/api/v2/operations", json=payload, verify=self.verify_ssl)
        if r.status_code in (200, 201):
            op_id = r.json().get("id")
            logger.info(f"🚀 Ability launched (operation: {op_id})")
            return {"success": True, "operation_id": op_id}
        return {"success": False, "error": r.text}
