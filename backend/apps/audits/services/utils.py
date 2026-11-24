import time

from src.outbound import fetch_public_url
from bs4 import BeautifulSoup


REQUEST_TIMEOUT = 15

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/138.0 Safari/537.36"
)


def normalize_url(url: str) -> str:
    """
    Ensure the URL has a scheme.
    """

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def fetch_page(url: str):
    """
    Download a web page and return:
    response,
    soup,
    elapsed_time
    """

    url = normalize_url(url)

    start = time.perf_counter()

    response = fetch_public_url(
        url,
        timeout=REQUEST_TIMEOUT,
        headers={
            "User-Agent": USER_AGENT,
        },

    )

    elapsed = round(time.perf_counter() - start, 2)

    soup = BeautifulSoup(response.text, "lxml")

    return response, soup, elapsed