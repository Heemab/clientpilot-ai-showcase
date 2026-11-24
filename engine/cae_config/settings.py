import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Central application configuration.

    Every module should import paths and
    configuration values from here.
    """

    # --------------------------------------------------
    # Project Paths
    # --------------------------------------------------

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    DATA_DIR = PROJECT_ROOT / "data"

    DATABASE_DIR = DATA_DIR / "database"

    REPORTS_DIR = PROJECT_ROOT / "reports"

    PROPOSALS_DIR = REPORTS_DIR / "proposals"

    OUTREACH_DIR = REPORTS_DIR / "outreach"

    LOGS_DIR = PROJECT_ROOT / "logs"

    EXPORTS_DIR = PROJECT_ROOT / "exports"

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    DATABASE_FILE = (
        DATABASE_DIR /
        "client_finder.db"
    )

    # --------------------------------------------------
    # APIs
    # --------------------------------------------------

    SERPAPI_API_KEY = os.getenv(
        "SERPAPI_API_KEY"
    )

    # Future APIs

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )

    GOOGLE_MAPS_API_KEY = os.getenv(
        "GOOGLE_MAPS_API_KEY"
    )

    GOOGLE_PLACES_API_KEY = os.getenv(
        "GOOGLE_PLACES_API_KEY"
    )

    # --------------------------------------------------
    # Proposal Defaults
    # --------------------------------------------------

    COMPANY_NAME = "ClientPilot"

    COMPANY_TITLE = (
        "AI Client Acquisition Engine"
    )

    CONSULTANT_TITLE = (
        "Digital Growth & Automation Consultant"
    )

    # --------------------------------------------------
    # Outreach
    # --------------------------------------------------

    DEFAULT_DISCOVERY_CALL = (
        "20-minute discovery call"
    )

    # --------------------------------------------------
    # Runtime
    # --------------------------------------------------

    DEBUG = (
        os.getenv(
            "DEBUG",
            "False",
        ).lower()
        == "true"
    )