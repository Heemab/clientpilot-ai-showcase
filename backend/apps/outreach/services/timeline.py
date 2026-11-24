from apps.outreach.models import OutreachEvent


class TimelineService:
    """
    Centralized service for recording outreach activity.
    """

    @staticmethod
    def log(
        outreach,
        event_type,
        user=None,
        notes="",
    ):
        return OutreachEvent.objects.create(
            outreach=outreach,
            event_type=event_type,
            created_by=user,
            notes=notes,
        )