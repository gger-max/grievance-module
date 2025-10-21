import os
from ulid import ULID  # <-- python-ulid API

PREFIX = os.getenv("GRIEVANCE_ID_PREFIX", "GRV-")

def new_grievance_id() -> str:
    return f"{PREFIX}{ULID()}"  # ULID() returns a ULID; str() happens implicitly
