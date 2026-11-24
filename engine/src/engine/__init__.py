"""
AI Client Acquisition Engine

Application Layer

Release
-------
v0.9.0

The engine is the public entry point into the
entire application.

External code should interact with CAEEngine
instead of directly calling repositories or
services.
"""

from .cae_engine import CAEEngine

__all__ = [
    "CAEEngine",
]

__version__ = "0.9.0"