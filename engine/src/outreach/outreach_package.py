from pathlib import Path
import json

from cae_config.settings import Settings

from src.outreach.outreach_generator import OutreachGenerator
from src.outreach.outreach_builder import OutreachBuilder
from src.database.outreach_repository import OutreachRepository


class OutreachPackage:
    """
    Creates a complete outreach package and
    registers it in the outreach repository.
    """

    def __init__(self):

        self.generator = OutreachGenerator()

        self.builder = OutreachBuilder()

        self.repository = OutreachRepository()

    # --------------------------------------------------
    # Build Package
    # --------------------------------------------------

    def build(
        self,
        opportunity,
        opportunity_id=None,
    ):

        outreach = self.generator.generate(
            opportunity
        )

        # ------------------------------------------
        # Register
        # ------------------------------------------

        record = self.repository.create(
            opportunity_id=opportunity_id or 0
        )

        outreach_number = record["outreach_number"]

        folder = (
            Settings.OUTREACH_DIR
            / outreach_number
        )

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ------------------------------------------
        # Build Files
        # ------------------------------------------

        files = {

            "email.txt":
                self.builder.build_email(outreach),

            "followup_1.txt":
                self.builder.build_followup_1(outreach),

            "followup_2.txt":
                self.builder.build_followup_2(outreach),

            "followup_3.txt":
                self.builder.build_followup_3(outreach),

            "linkedin.txt":
                self.builder.build_linkedin(outreach),

            "whatsapp.txt":
                self.builder.build_whatsapp(outreach),

            "call_script.txt":
                self.builder.build_call_script(outreach),

            "README.md":
                self.builder.build_readme(outreach),

        }

        for filename, content in files.items():

            with open(

                folder / filename,

                "w",

                encoding="utf-8",

            ) as f:

                f.write(content)

        # ------------------------------------------
        # JSON
        # ------------------------------------------

        json_path = (
            folder /
            "outreach.json"
        )

        with open(

            json_path,

            "w",

            encoding="utf-8",

        ) as f:

            json.dump(

                {

                    "business_name":
                        outreach.business_name,

                    "category":
                        outreach.category,

                    "priority":
                        outreach.priority,

                    "primary_service":
                        outreach.primary_service,

                    "estimated_value":
                        outreach.estimated_value,

                    "roi_score":
                        outreach.roi_score,

                    "strategy":
                        outreach.strategy,

                    "call_to_action":
                        outreach.call_to_action,

                },

                f,

                indent=4,

                ensure_ascii=False,

            )

        # ------------------------------------------
        # Update Repository
        # ------------------------------------------

        self.repository.update_paths(

            record["id"],

            folder_path=str(folder),

            json_path=str(json_path),

        )

        return {

            "outreach":
                outreach,

            "record":
                record,

            "folder":
                str(folder),

            "json":
                str(json_path),

        }