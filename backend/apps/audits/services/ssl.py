from urllib.parse import urlparse

from src.outbound import fetch_public_url


def analyze_ssl(original_url, response):
    """
    Determine SSL usage and HTTP→HTTPS redirect.
    """

    result = {
        "ssl_enabled": False,
        "https_redirect": False,
    }

    final_url = response.url

    if urlparse(final_url).scheme == "https":
        result["ssl_enabled"] = True

    try:
        parsed = urlparse(original_url)

        if parsed.scheme == "https":
            http_url = original_url.replace(
                "https://",
                "http://",
                1,
            )
        else:
            http_url = original_url

        redirect_response = fetch_public_url(
            http_url,

            timeout=10,
        )

        if redirect_response.url.startswith("https://"):
            result["https_redirect"] = True

    except Exception:
        pass

    return result