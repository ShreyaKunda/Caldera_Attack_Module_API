from src.attack_engine import AttackEngine
from src.caldera_client import CalderaClient
import json

config = json.load(open("config/settings.json"))
client = CalderaClient(config)
engine = AttackEngine(client)

print(engine.execute_random_attack())
