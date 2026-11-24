from __future__ import annotations

from src.outbound import fetch_public_url
from bs4 import BeautifulSoup

from src.models.audit_context import AuditContext
from src.models.opportunity import Opportunity


class AuditContextBuilder:
    """
    Builds an AuditContext from an Opportunity.

    Responsible for downloading and parsing the target website.
    """

    DEFAULT_TIMEOUT = 15

    def build(
        self,
        opportunity: Opportunity,
    ) -> AuditContext:

        response = fetch_public_url(
            opportunity.website,
            timeout=self.DEFAULT_TIMEOUT,
            headers={
                "User-Agent": (
                    "ClientPilotAI/1.0 "
                    "(Website Audit Bot)"
                )
            },
        )

        response.raise_for_status()

        html = response.text

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        return AuditContext(
            url=response.url,
            response=response,
            html=html,
            soup=soup,
        )