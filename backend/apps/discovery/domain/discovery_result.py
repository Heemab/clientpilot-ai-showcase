from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class DiscoveryResult:
    """
    Canonical discovery result shared by all discovery providers.

    Every discovery integration (Google Maps, LinkedIn, Freelancer,
    Guru, PeoplePerHour, Apollo, CSV imports, etc.) should normalize
    its raw response into this immutable value object before passing
    it further into the discovery pipeline.

    This object intentionally contains only CRM-relevant fields.
    Provider-specific metadata should remain inside the provider
    implementation unless there is a business need to expose it.
    """

    source: str
    business_name: str

    category: str = ""
    address: str = ""
    phone: str = ""
    website: str = ""
    rating: float = 0.0
    reviews: int = 0

    def to_dict(self) -> dict[str, Any]:
        """
        Convert this DiscoveryResult into a JSON-serializable dictionary.

        Used when storing discovery results in the user's session.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DiscoveryResult":
        """
        Recreate a DiscoveryResult from a dictionary.

        Used when reading discovery results back from the session.
        """
        return cls(**data)