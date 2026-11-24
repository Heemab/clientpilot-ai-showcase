"""
Pricing Engine

Calculates implementation pricing
based on estimated effort, CMS complexity,
and agency hourly rate.
"""

from .effort import estimate_effort

# ---------------------------------------------------------
# Agency Settings
# ---------------------------------------------------------

DEFAULT_HOURLY_RATE = 125

MINIMUM_SERVICE_PRICE = 150


# ---------------------------------------------------------
# CMS Complexity
# ---------------------------------------------------------

def cms_multiplier(cms):
    """
    Complexity multiplier by CMS.
    """

    cms = (cms or "").lower()

    multipliers = {
        "wordpress": 1.00,
        "wix": 0.80,
        "shopify": 1.20,
        "drupal": 1.35,
        "joomla": 1.15,
        "squarespace": 0.90,
    }

    return multipliers.get(cms, 1.00)


# ---------------------------------------------------------
# Pricing
# ---------------------------------------------------------

def estimate_service_price(service, results):
    """
    Estimate implementation price.
    """

    multiplier = cms_multiplier(
        results.get("cms")
    )

    hours = estimate_effort(
        service,
        results,
    )

    hourly_rate = DEFAULT_HOURLY_RATE

    price = (
        hours
        * hourly_rate
        * multiplier
    )

    # ---------------------------------------------
    # Minimum pricing safeguard
    # ---------------------------------------------

    if price < MINIMUM_SERVICE_PRICE:
        price = MINIMUM_SERVICE_PRICE

    return round(price)