from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from src.models.business_assessment import BusinessAssessment

@dataclass
class Opportunity:
    """
    Standard opportunity model used throughout the application.

    Every connector (Google Maps, Yelp, LinkedIn, etc.)
    returns this model.
    """

    # --------------------------------------------------
    # Source Information
    # --------------------------------------------------

    source: str
    business_name: str
    category: str
    address: str
    phone: str
    website: str

    # --------------------------------------------------
    # Google Business Profile
    # --------------------------------------------------

    rating: float
    reviews: int

    # --------------------------------------------------
    # Opportunity Intelligence
    # --------------------------------------------------

    opportunity_score: int = 0

    technology: str = "Unknown"

    priority: str = "MEDIUM"

    recommended_services: str = ""

    # --------------------------------------------------
    # Website Intelligence
    # --------------------------------------------------

    # Raw analyzer report
    website_report: dict = field(default_factory=dict)

    # Legacy human-readable findings
    website_findings: list = field(default_factory=list)

    # NEW: Structured findings for proposals
    website_structured_findings: list = field(default_factory=list)

    # Persisted JSON copies
    website_report_json: str = ""

    website_findings_json: str = ""

    website_structured_findings_json: str = ""

    # --------------------------------------------------
    # Business Intelligence
    # --------------------------------------------------

    primary_service: str = ""

    estimated_value: int = 0

    estimated_hours: int = 0

    difficulty: str = "Easy"

    closing_probability: int = 0

    roi_score: int = 0

    sales_reason: str = ""

    # --------------------------------------------------
    # CRM
    # --------------------------------------------------

    status: str = "NEW"

    last_contacted: str = ""

    follow_up_date: str = ""

    notes: str = ""

    # --------------------------------------------------
    # Contact Intelligence
    # --------------------------------------------------

    business_email: str = ""

    contact_page: str = ""

    facebook_url: str = ""

    linkedin_url: str = ""

    instagram_url: str = ""

    owner_name: str = ""

    # --------------------------------------------------
    # Assessment
    # --------------------------------------------------

    business_assessment: Optional[BusinessAssessment] = None

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    created_at: datetime = field(default_factory=datetime.now)