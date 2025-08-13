# Caldera Attack Module

A Python wrapper and interactive CLI for automating **MITRE Caldera** adversary emulation via its REST API.

With this, you can:
- Authenticate with an **API key** 
- Enumerate **agents**, **adversaries**, **abilities**, and **planners**
- Launch **operations** interactively or in one go from the CLI
- Choose **adversary** and **planner** at runtime

---

##  Project Structure

```
src/
  ├─ caldera_attack_module.py   # Core API wrapper
  └─ __init__.py
example_usage.py                # CLI interface (basic + interactive)
requirements.txt
README.md
```

---

##  Requirements

- Python 3.9+
- A running **Caldera** server (v5+)
- API key from your Caldera `conf/default.yml`
  - `api_key_red` (e.g. `ADMIN123`) or `api_key_blue` (e.g. `BLUEADMIN123`)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

##  Configuration

Edit `example_usage.py`:

```python
SERVER_URL = "http://<your-caldera-ip>:8888"
API_KEY    = "ADMIN123"  # from conf/default.yml
VERIFY_SSL = False
```

---

##  Usage

### Basic mode

```bash
python example_usage.py
```

Runs a default operation with:
- First available agent
- First available adversary
- First available planner

### Interactive mode

```bash
python example_usage.py --interactive
```

You can:
1. List agents
2. List adversaries
3. List abilities
4. Run an operation by:
   - Naming it
   - Picking an adversary
   - Picking a planner
5. Exit cleanly

---

##  How it works

- Authenticates with `KEY: <API_KEY>` header
- Retrieves resources via:
  - `/api/v2/agents`
  - `/api/v2/adversaries`
  - `/api/v2/abilities`
  - `/api/v2/planners`
- Creates operations with a valid `planner.id` (avoids `422: Field may not be null` errors)

Example operation payload:

```json
{
  "name": "Test_Op",
  "adversary": { "adversary_id": "<uuid>" },
  "planner":   { "id": "<planner-uuid>" },
  "state": "running",
  "autonomous": 1,
  "host_group": "red"
}
```

---

##  Manual API checks

List planners:

```bash
curl -H "KEY: ADMIN123" http://<caldera-ip>:8888/api/v2/planners
```

List adversaries:

```bash
curl -H "KEY: ADMIN123" http://<caldera-ip>:8888/api/v2/adversaries
```

