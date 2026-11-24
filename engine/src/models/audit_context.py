from dataclasses import dataclass

from bs4 import BeautifulSoup
from requests import Response


@dataclass(slots=True)
class AuditContext:
    """
    Shared context passed to every audit module.

    This avoids passing multiple arguments
    (url, html, soup, response, etc.) to every audit.
    """

    url: str

    response: Response

    html: str

    soup: BeautifulSoup

    @property
    def headers(self):
        return self.response.headers

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def elapsed_ms(self):
        return int(
            self.response.elapsed.total_seconds() * 1000
        )