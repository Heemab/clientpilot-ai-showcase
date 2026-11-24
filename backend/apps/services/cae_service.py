from functools import lru_cache

from src.engine.cae_engine import CAEEngine


@lru_cache(maxsize=1)
def get_engine() -> CAEEngine:
    """
    Returns the singleton ClientPilot AI engine instance.

    The engine is created once per Django process and reused
    across incoming requests.
    """
    return CAEEngine()