from src.outbound import fetch_public_url
from bs4 import BeautifulSoup

from src.detectors.technology_detector import TechnologyDetector

from src.models.audit_context import AuditContext
from src.models.website_report import WebsiteReport

from src.audit.security_audit import SecurityAudit


class WebsiteAnalyzer:
    """
    Website Analyzer (v2)

    Responsibilities
    ----------------
    • Download webpage
    • Build AuditContext
    • Execute registered audits
    • Produce WebsiteReport
    • Preserve legacy report structure
    """

    def __init__(self):

        self.technology_detector = TechnologyDetector()

        # --------------------------------------------------
        # Registered audits
        # --------------------------------------------------

        self.audits = [

            SecurityAudit(),

        ]

    # --------------------------------------------------

    def analyze(self, url):

        # --------------------------------------------------
        # Legacy report (kept for compatibility)
        # --------------------------------------------------

        report = {

            "website_exists": False,

            "https": False,

            "title": "",

            "meta_description": "",

            "email_found": False,

            "contact_form": False,

            "technology": "Unknown",

            # NEW
            "structured_report": None,

        }

        if not url:

            return report

        try:

            response = fetch_public_url(

                url,

                timeout=10,

                headers={

                    "User-Agent": (

                        "Mozilla/5.0 "

                        "(Windows NT 10.0; Win64; x64)"

                    )

                },

            )

            html = response.text

            soup = BeautifulSoup(

                html,

                "lxml",

            )

            technology = self.technology_detector.detect(

                html

            )

            # --------------------------------------------------
            # Populate legacy report
            # --------------------------------------------------

            report["website_exists"] = True

            report["https"] = url.lower().startswith(

                "https://"

            )

            report["technology"] = technology

            if soup.title:

                report["title"] = (

                    soup.title.text.strip()

                )

            meta = soup.find(

                "meta",

                attrs={

                    "name": "description"

                }

            )

            if meta:

                report["meta_description"] = (

                    meta.get(

                        "content",

                        ""

                    )

                )

            report["email_found"] = (

                "@" in html

            )

            report["contact_form"] = (

                soup.find("form") is not None

            )

            # --------------------------------------------------
            # Build Audit Context
            # --------------------------------------------------

            context = AuditContext(

                url=url,

                response=response,

                html=html,

                soup=soup,

            )

            # --------------------------------------------------
            # Structured Website Report
            # --------------------------------------------------

            website_report = WebsiteReport(

                url=url,

                technology=technology,

            )

            total_score = 0

            completed = 0

            # --------------------------------------------------
            # Execute registered audits
            # --------------------------------------------------

            for audit in self.audits:

                result = audit.analyze(

                    context

                )

                completed += 1

                total_score += result.score

                audit_name = (

                    audit.name

                    .lower()

                    .replace(

                        " audit",

                        ""

                    )

                )

                if hasattr(

                    website_report,

                    audit_name,

                ):

                    setattr(

                        website_report,

                        audit_name,

                        result,

                    )

            if completed:

                website_report.overall_score = int(

                    total_score / completed

                )

            report["structured_report"] = (

                website_report

            )

        except Exception as e:

            print("\nWebsiteAnalyzer Error")
            print(type(e).__name__)
            print(e)

            raise

        return report