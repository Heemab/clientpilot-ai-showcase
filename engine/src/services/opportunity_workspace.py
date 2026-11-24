from src.database.workspace_repository import WorkspaceRepository
from src.services.ai_outreach_generator import AIOutreachGenerator


class OpportunityWorkspace:
    """
    Builds a complete workspace for an opportunity.

    This is the central service used by every
    future module (CRM, Proposal Generator,
    Email Sender, Dashboard, etc.).
    """

    def __init__(self):

        self.repository = WorkspaceRepository()

        self.outreach = AIOutreachGenerator()

    # --------------------------------------------------
    # Load Workspace
    # --------------------------------------------------

    def load(self, opportunity_id):
        """
        Load a complete workspace by opportunity ID.
        """

        workspace = self.repository.get_by_id(
            opportunity_id
        )

        if workspace is None:

            return None

        opportunity = workspace["opportunity"]

        outreach = self.outreach.generate(
            opportunity
        )

        workspace["outreach"] = outreach

        return workspace

    # --------------------------------------------------
    # Best Opportunity
    # --------------------------------------------------

    def best(self):
        """
        Load the highest-value opportunity.
        """

        workspace = self.repository.get_best()

        if workspace is None:

            return None

        opportunity = workspace["opportunity"]

        workspace["outreach"] = self.outreach.generate(
            opportunity
        )

        return workspace

    # --------------------------------------------------
    # Latest Opportunities
    # --------------------------------------------------

    def latest(self, limit=10):
        """
        Load the latest opportunities.
        """

        workspaces = []

        opportunities = self.repository.latest(limit)

        for workspace in opportunities:

            opportunity = workspace["opportunity"]

            workspace["outreach"] = (
                self.outreach.generate(
                    opportunity
                )
            )

            workspaces.append(
                workspace
            )

        return workspaces

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self, workspace):
        """
        Returns a lightweight summary.
        """

        opportunity = workspace["opportunity"]

        return {

            "Business": opportunity.business_name,

            "Technology": opportunity.technology,

            "Priority": opportunity.priority,

            "Score": opportunity.opportunity_score,

            "Primary Service": opportunity.primary_service,

            "Estimated Value": opportunity.estimated_value,

            "Estimated Hours": opportunity.estimated_hours,

            "Difficulty": opportunity.difficulty,

            "Closing Probability": opportunity.closing_probability,

            "ROI": opportunity.roi_score,

            "Status": opportunity.status,

        }