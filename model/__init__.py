import json
import logging
import os
from pathlib import Path


logger = logging.getLogger(__name__)
logging.basicConfig()

REPO_DIR = Path(__file__).parent.parent


if Path(REPO_DIR / "secrets.json").exists():
    logger.info("Reading secrets into environment variables...")
    secrets = json.loads(Path(REPO_DIR / "secrets.json").read_text())
    for k, v in secrets.items():
        os.environ[k] = v
