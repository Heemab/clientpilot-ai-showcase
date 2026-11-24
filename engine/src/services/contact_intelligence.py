import re

from src.outbound import fetch_public_url
from bs4 import BeautifulSoup

from src.models.contact_information import ContactInformation


class ContactIntelligence:
    """
    Discovers basic contact information from a
    business website.

    CAE v1.0

    Extracts:
    - Business Email
    - Contact Page

    Future Versions
    ---------------
    - Facebook
    - LinkedIn
    - Instagram
    - Owner
    """

    EMAIL_PATTERN = re.compile(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    )

    def discover(
        self,
        website,
    ):

        contact = ContactInformation()

        if not website:

            return contact

        try:

            response = fetch_public_url(

                website,

                timeout=10,

                headers={

                    "User-Agent":
                    (
                        "Mozilla/5.0"
                    )

                },

            )

            soup = BeautifulSoup(

                response.text,

                "html.parser",

            )

            # ------------------------------------------
            # Email
            # ------------------------------------------

            emails = set(

                self.EMAIL_PATTERN.findall(
                    response.text
                )

            )

            emails = {

                email

                for email in emails

                if "example.com" not in email.lower()

            }

            if emails:

                contact.business_email = sorted(
                    emails
                )[0]

            # ------------------------------------------
            # Contact Page
            # ------------------------------------------

            for link in soup.find_all(

                "a",

                href=True,

            ):

                href = link["href"]

                text = link.get_text(
                    strip=True
                ).lower()

                href_lower = href.lower()

                if (

                    "contact" in text

                    or

                    "contact" in href_lower

                ):

                    if href.startswith("http"):

                        contact.contact_page = href

                    else:

                        contact.contact_page = (

                            website.rstrip("/")

                            + "/"

                            + href.lstrip("/")

                        )

                    break

        except Exception:

            # Ignore failures.
            # Missing contact information should
            # never stop the pipeline.
            pass

        return contact