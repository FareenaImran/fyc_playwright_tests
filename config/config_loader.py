import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / "config" / ".env"
load_dotenv(dotenv_path=env_path)
env=os.getenv("ENV","beta").lower()

if env=="beta":
    from config.environments.beta import *
else:
    from config.environments.staging import *

print()
print("="*60)
print(f"ENVIRONMENT :  {ENV_NAME}")
print("="*60)