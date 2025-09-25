import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
env=os.getenv("ENV","beta").lower()    #default value is beta

if env=="beta":
    from config.environments.beta import *
else:
    from config.environments.staging import *

print()
print("="*60)
print(f"ENVIRONMENT :  {ENV_NAME}")
print("="*60)