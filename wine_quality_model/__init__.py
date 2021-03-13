import os
import json
from pathlib import Path

if Path("secrets.json").exists():
    secrets = json.loads(Path("secrets.json").read_text())
    for k, v in secrets.items():
        os.environ[k] = v
