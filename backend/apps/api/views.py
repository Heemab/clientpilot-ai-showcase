import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.services.cae_service import get_engine

logger = logging.getLogger(__name__)


class EngineAPIView(APIView):
    """
    Base API view for all ClientPilot Engine endpoints.
    Provides shared engine access and consistent error handling.
    """

    permission_classes = []

    @property
    def engine(self):
        return get_engine()

    def execute(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception("ClientPilot Engine execution failed.")
            return Response(
                {
                    "detail": "Internal engine error."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EngineHealthView(EngineAPIView):

    def get(self, request):
        return Response(
            {
                "status": "healthy",
                "engine": self.engine.__class__.__name__,
                "version": "0.1.0",
            }
        )


class DashboardView(EngineAPIView):

    def get(self, request):
        result = self.execute(self.engine.dashboard)

        if isinstance(result, Response):
            return result

        return Response(result)


class BestOpportunityView(EngineAPIView):

    def get(self, request):
        result = self.execute(self.engine.best_opportunity)

        if isinstance(result, Response):
            return result

        if result is None:
            return Response(
                {
                    "detail": "No opportunities found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(result)


class ProposalView(EngineAPIView):

    def post(self, request):
        opportunity_id = request.data.get("opportunity_id")

        if not opportunity_id:
            return Response(
                {
                    "detail": "opportunity_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = self.execute(
            self.engine.generate_proposal,
            opportunity_id,
        )

        if isinstance(result, Response):
            return result

        if result is None:
            return Response(
                {
                    "detail": "Opportunity not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(result)