from dataclasses import dataclass

from src.database.workspace_repository import WorkspaceRepository
from src.services.opportunity_processor import OpportunityProcessor
from src.proposals.proposal_package import ProposalPackage
from src.outreach.outreach_package import OutreachPackage


@dataclass(slots=True)
class ClientWorkflowResult:
    """
    Result returned after executing the complete
    client workflow.
    """

    success: bool

    message: str

    opportunity: object = None

    proposal_package: dict = None

    outreach_package: dict = None


class ClientWorkflow:
    """
    Executes the complete client acquisition workflow.

    Pipeline

        Load Opportunity
                ↓
        Website Analysis
                ↓
        Business Assessment
                ↓
        Proposal Package
                ↓
        Outreach Package
                ↓
        Return Result
    """

    def __init__(self):

        self.workspace = WorkspaceRepository()

        self.processor = OpportunityProcessor()

        self.proposal_package = ProposalPackage()

        self.outreach_package = OutreachPackage()

    # --------------------------------------------------

    def run(
        self,
        opportunity_id,
    ):

        workspace = self.workspace.get_by_id(
            opportunity_id
        )

        if workspace is None:

            return ClientWorkflowResult(

                success=False,

                message="Opportunity not found."

            )

        opportunity = workspace["opportunity"]

        # ------------------------------------------
        # Process Opportunity
        # ------------------------------------------

        opportunity = self.processor.process(
            opportunity
        )

        # ------------------------------------------
        # Proposal Package
        # ------------------------------------------

        proposal = self.proposal_package.build(

            opportunity,

            opportunity_id,

        )

        # ------------------------------------------
        # Outreach Package
        # ------------------------------------------

        outreach = self.outreach_package.build(

            opportunity,

            opportunity_id,

        )

        # ------------------------------------------

        return ClientWorkflowResult(

            success=True,

            message="Workflow completed successfully.",

            opportunity=opportunity,

            proposal_package=proposal,

            outreach_package=outreach,

        )