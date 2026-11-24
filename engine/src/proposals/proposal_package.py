from pathlib import Path
import json

from cae_config.settings import Settings

from src.database.proposal_repository import ProposalRepository
from src.proposals.proposal_generator import ProposalGenerator
from src.proposals.proposal_builder import ProposalBuilder
from src.proposals.proposal_exporter import ProposalExporter


class ProposalPackage:
    """
    Coordinates the creation of a complete proposal package.

    Current Package
    ---------------
    • Proposal.md
    • proposal.json
    • client.json

    Future Package
    --------------
    • Proposal.pdf
    • Proposal.docx
    • Email.txt
    • Website Report
    • Findings Report
    """

    def __init__(self):

        self.generator = ProposalGenerator()

        self.builder = ProposalBuilder()

        self.exporter = ProposalExporter()

        self.repository = ProposalRepository()

        # --------------------------------------------------
        # Build Complete Package
        # --------------------------------------------------

    def build(
        self,
        opportunity,
        opportunity_id=None,
        scoring_result=None,
    ):
        """
        Generate a complete proposal package.
        """

        # --------------------------------------------------
        # Generate Proposal Data
        # --------------------------------------------------

        proposal = self.generator.generate(
            opportunity,
            scoring_result=scoring_result,
        )

        # --------------------------------------------------
        # Register Proposal
        # --------------------------------------------------

        proposal_record = self.repository.create(

            opportunity_id=opportunity_id or 0

        )

        proposal["proposal_number"] = (
            proposal_record["proposal_number"]
        )

        proposal["proposal_status"] = (
            proposal_record["status"]
        )

        # --------------------------------------------------
        # Create Proposal Folder
        # --------------------------------------------------

        package_folder = (

            Settings.PROPOSALS_DIR /

            proposal["proposal_number"]

        )

        package_folder.mkdir(

            parents=True,

            exist_ok=True,

        )

        # --------------------------------------------------
        # Build Markdown
        # --------------------------------------------------

        markdown = self.builder.build(
            proposal
        )

        # --------------------------------------------------
        # Export Markdown
        # --------------------------------------------------

        markdown_path = (

            package_folder /

            "Proposal.md"

        )

        self.exporter.export_markdown(

            markdown,

            markdown_path,

        )

        # --------------------------------------------------
        # Export Proposal JSON
        # --------------------------------------------------

        json_path = (

            package_folder /

            "proposal.json"

        )

        with open(

            json_path,

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                proposal,

                file,

                indent=4,

                ensure_ascii=False,

            )

        # --------------------------------------------------
        # Export Client JSON
        # --------------------------------------------------

        client_json_path = (

            package_folder /

            "client.json"

        )

        client_information = {

            "business_name":
                opportunity.business_name,

            "category":
                opportunity.category,

            "website":
                opportunity.website,

            "phone":
                opportunity.phone,

            "business_email":
                getattr(
                    opportunity,
                    "business_email",
                    "",
                ),

            "contact_page":
                getattr(
                    opportunity,
                    "contact_page",
                    "",
                ),

            "facebook_url":
                getattr(
                    opportunity,
                    "facebook_url",
                    "",
                ),

            "linkedin_url":
                getattr(
                    opportunity,
                    "linkedin_url",
                    "",
                ),

            "instagram_url":
                getattr(
                    opportunity,
                    "instagram_url",
                    "",
                ),

            "owner_name":
                getattr(
                    opportunity,
                    "owner_name",
                    "",
                ),

        }

        with open(

            client_json_path,

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                client_information,

                file,

                indent=4,

                ensure_ascii=False,

            )

        # --------------------------------------------------
        # Update Proposal Record
        # --------------------------------------------------

        self.repository.update_paths(

            proposal_record["id"],

            markdown_path=str(markdown_path),

            pdf_path="",

        )

        # --------------------------------------------------
        # Return Package Information
        # --------------------------------------------------

        return {

            "proposal": proposal,

            "proposal_record": proposal_record,

            "markdown": markdown,

            "markdown_path": str(markdown_path),

            "package_folder": str(package_folder),

            "json_path": str(json_path),

            "client_json_path": str(client_json_path),

        }