from dataclasses import FrozenInstanceError
from unittest import TestCase

from apps.discovery.domain.discovery_result import DiscoveryResult


class DiscoveryResultTests(TestCase):
    def test_defaults(self):
        result = DiscoveryResult(source="Google Maps", business_name="Acme Dental")

        self.assertEqual(result.source, "Google Maps")
        self.assertEqual(result.business_name, "Acme Dental")
        self.assertEqual(result.category, "")
        self.assertEqual(result.address, "")
        self.assertEqual(result.phone, "")
        self.assertEqual(result.website, "")
        self.assertEqual(result.rating, 0.0)
        self.assertEqual(result.reviews, 0)

    def test_is_immutable(self):
        result = DiscoveryResult(source="Google Maps", business_name="Acme Dental")

        with self.assertRaises(FrozenInstanceError):
            result.business_name = "New Name"
