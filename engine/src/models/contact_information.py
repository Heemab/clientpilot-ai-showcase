from dataclasses import dataclass


@dataclass(slots=True)
class ContactInformation:
    """
    Stores the primary contact information
    discovered from a business website.

    v1.0 only captures the essentials needed
    to contact a prospect.
    """

    # --------------------------------------------------
    # Contact Details
    # --------------------------------------------------

    business_email: str = ""

    contact_page: str = ""

    # --------------------------------------------------
    # Convenience
    # --------------------------------------------------

    @property
    def has_email(self) -> bool:

        return bool(self.business_email.strip())

    @property
    def has_contact_page(self) -> bool:

        return bool(self.contact_page.strip())