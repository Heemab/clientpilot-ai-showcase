from src.audit.audit_context_builder import AuditContextBuilder
from src.audit.audit_package import AuditPackage

from src.database.workspace_repository import WorkspaceRepository

from src.proposals.proposal_package import ProposalPackage
from src.scoring.opportunity_scorer import OpportunityScorer
from src.outreach.outreach_package import OutreachPackage


class CAEEngine:
    """
    ClientPilot AI Client Acquisition Engine.

    Public application facade.

    Coordinates feature packages while keeping all
    business logic inside their respective modules.
    """

    def __init__(self):

        self.workspace = WorkspaceRepository()

        self.audit_context_builder = AuditContextBuilder()

        self.audit_package = AuditPackage()

        self.proposal_package = ProposalPackage()

        self.opportunity_scorer = OpportunityScorer()

        self.outreach_package = OutreachPackage()

    # --------------------------------------------------
    # Best Opportunity
    # --------------------------------------------------

    def best_opportunity(self):
        """
        Return the highest-ranked opportunity.
        """

        return self.workspace.get_best()

    # --------------------------------------------------
    # Load Opportunity
    # --------------------------------------------------

    def load(
        self,
        opportunity_id,
    ):
        """
        Load workspace by opportunity ID.
        """

        return self.workspace.get_by_id(
            opportunity_id
        )

    # --------------------------------------------------
    # Website Audit
    # --------------------------------------------------

    def audit(
        self,
        opportunity_id,
    ):
        """
        Execute every audit module for a website.
        """

        workspace = self.load(opportunity_id)

        if workspace is None:
            return None

        context = self.audit_context_builder.build(
            workspace["opportunity"]
        )

        return self.audit_package.analyze(
            context
        )

    # --------------------------------------------------
    # Opportunity Score
    # --------------------------------------------------

    def score(
        self,
        opportunity_id,
    ):
        """
        Calculate opportunity score.
        """

        workspace = self.load(opportunity_id)

        if workspace is None:
            return None

        audit_report = self.audit(opportunity_id)

        if audit_report is None:
            return None

        return self.opportunity_scorer.score(
            workspace["opportunity"],
            audit_report,
        )

    # --------------------------------------------------
    # Proposal Generation
    # --------------------------------------------------

    def generate_proposal(
        self,
        opportunity_id,
    ):
        """
        Generate complete proposal package.
        """

        workspace = self.load(opportunity_id)

        if workspace is None:
            return None

        scoring_result = self.score(
            opportunity_id
        )

        return self.proposal_package.build(
            workspace["opportunity"],
            workspace["id"],
            scoring_result=scoring_result,
        )

    # --------------------------------------------------
    # Outreach Generation
    # --------------------------------------------------

    def generate_outreach(
        self,
        opportunity_id,
    ):
        """
        Generate outreach package.
        """

        workspace = self.load(opportunity_id)

        if workspace is None:
            return None

        return self.outreach_package.build(
            workspace["opportunity"],
            workspace["id"],
        )

    # --------------------------------------------------
    # Complete Workflow
    # --------------------------------------------------

    def run(
        self,
        opportunity_id,
    ):
        """
        Execute the complete ClientPilot workflow.
        """

        workspace = self.load(opportunity_id)

        if workspace is None:
            return None

        audit_report = self.audit(
            opportunity_id
        )

        scoring_result = self.score(
            opportunity_id
        )

        proposal = self.generate_proposal(
            opportunity_id
        )

        outreach = self.generate_outreach(
            opportunity_id
        )

        return {
            "workspace": workspace,
            "audit_report": audit_report,
            "scoring_result": scoring_result,
            "proposal": proposal,
            "outreach": outreach,
        }

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    def dashboard(self):
        """
        Dashboard summary.
        """

        workspace = self.best_opportunity()

        if workspace is None:

            return {
                "total_opportunities": 0,
                "best_opportunity": None,
                "priority": None,
                "roi_score": None,
            }

        scoring_result = self.score(
            workspace["id"]
        )

        opportunity = workspace["opportunity"]

        return {
            "total_opportunities": len(
                self.workspace.latest(10)
            ),
            "best_opportunity": opportunity.business_name,
            "priority": (
                scoring_result.priority
                if scoring_result
                else None
            ),
            "roi_score": (
                scoring_result.score
                if scoring_result
                else None
            ),
        }