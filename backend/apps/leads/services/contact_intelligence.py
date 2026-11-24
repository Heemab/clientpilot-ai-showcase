import re
from dataclasses import dataclass

from urllib.parse import urljoin

from requests.exceptions import RequestException
from src.outbound import fetch_public_url
from bs4 import BeautifulSoup


@dataclass(slots=True)
class ContactInfo:
    business_email: str | None = None
    contact_page: str | None = None


class ContactIntelligence:
    """
    Discovers contact information from a business website.

    Extracts:
    - Business Email
    - Contact Page

    Future:
    - Phone
    - LinkedIn
    - Facebook
    - Instagram
    """

    EMAIL_PATTERN = re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/126.0 Safari/537.36"
        )
    }

    def _extract_emails(self, html: str) -> list[str]:
        emails = {
            email
            for email in self.EMAIL_PATTERN.findall(html)
            if "example.com" not in email.lower()
        }
        return sorted(emails)

    def discover(self, lead) -> ContactInfo:
        contact = ContactInfo()

        website = lead.website

        if not website:
            return contact

        try:
            response = fetch_public_url(
                website,
                timeout=10,
                headers=self.HEADERS,
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser",
            )

            # Homepage email
            emails = self._extract_emails(response.text)

            if emails:
                contact.business_email = emails[0]

            # Find Contact page
            for link in soup.find_all("a", href=True):
                href = link["href"]
                text = link.get_text(strip=True).lower()

                if (
                    "contact" in text
                    or "contact" in href.lower()
                ):

                    if href.startswith("http"):
                        contact.contact_page = href
                    else:
                        contact.contact_page = urljoin(response.url, href)

                    break

            # Search Contact page if homepage had no email
            if (
                not contact.business_email
                and contact.contact_page
            ):
                response = fetch_public_url(
                    contact.contact_page,
                    timeout=10,
                    headers=self.HEADERS,
                )

                response.raise_for_status()

                emails = self._extract_emails(response.text)

                if emails:
                    contact.business_email = emails[0]

        except RequestException:
            pass

        return contact