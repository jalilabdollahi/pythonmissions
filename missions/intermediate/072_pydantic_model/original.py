# Mission 072 - Pydantic Model
# Fix the 2 bugs in this script.
try:
    from pydantic import BaseModel, validator
    from typing import Optional, List
except ImportError:
    # Stub for environments without pydantic
    class BaseModel:
        def __init__(self, **kw):
            for k, v in kw.items(): setattr(self, k, v)
    def validator(*a, **kw):
        def decorator(fn): return fn
        return decorator
    from typing import Optional, List

class DeployRequest(BaseModel):
    service: str
    version: str
    replicas: int = 1
    env: str = "prod"
    tags: List[str] = []

    @validator("version")
    def version_must_start_with_v(cls, v):
        if not v.startswith("v"):
            raise ValueError("version must start with v")
        return v

    @validator("service")
    def service_not_empty(cls, v):
        if not v.strip():
            raise ValueError("service cannot be empty")
        return v.strip()
