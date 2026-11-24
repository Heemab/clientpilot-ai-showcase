import json

from src.database.database import Database
from src.models.opportunity import Opportunity
from src.services.opportunity_processor import OpportunityProcessor


class WorkspaceRepository:
    """
    Repository responsible for loading a complete
    Opportunity Workspace.

    Unlike a simple repository, this class rebuilds
    the complete Opportunity object by re-running the
    OpportunityProcessor so that BusinessAssessment
    and proposal data are always current.
    """

    def __init__(self):

        self.db = Database()

        self.processor = OpportunityProcessor()

    # --------------------------------------------------
    # Load Opportunity
    # --------------------------------------------------

    def get_by_id(self, opportunity_id):

        connection = self.db.connect()

        connection.row_factory = lambda cursor, row: {

            cursor.description[idx][0]: row[idx]

            for idx in range(len(cursor.description))

        }

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM opportunities

            WHERE id = ?
            """,
            (opportunity_id,),
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:

            return None

        opportunity = Opportunity(

            source=row["source"],

            business_name=row["business_name"],

            category=row["category"],

            address=row["address"],

            phone=row["phone"],

            website=row["website"],

            rating=row["rating"],

            reviews=row["reviews"],

            opportunity_score=row["opportunity_score"],

            technology=row["technology"],

            priority=row["priority"],

            recommended_services=row["recommended_services"] or "",

            primary_service=row["primary_service"],

            estimated_value=row["estimated_value"],

            estimated_hours=row["estimated_hours"],

            difficulty=row["difficulty"],

            closing_probability=row["closing_probability"],

            roi_score=row["roi_score"],

            sales_reason=row["sales_reason"],

            status=row["status"],

            last_contacted=row["last_contacted"] or "",

            follow_up_date=row["follow_up_date"] or "",

            notes=row["notes"] or "",

        )

        # --------------------------------------------------
        # Restore Persisted Website Intelligence
        # --------------------------------------------------

        opportunity.website_report_json = (
            row.get("website_report_json") or ""
        )

        opportunity.website_findings_json = (
            row.get("website_findings_json") or ""
        )

        opportunity.website_structured_findings_json = (
            row.get("website_structured_findings_json") or ""
        )

        # --------------------------------------------------
        # Restore Lists (Legacy)
        # --------------------------------------------------

        try:

            if opportunity.website_findings_json:

                opportunity.website_findings = json.loads(
                    opportunity.website_findings_json
                )

        except Exception:

            opportunity.website_findings = []

        try:

            if opportunity.website_structured_findings_json:

                opportunity.website_structured_findings = json.loads(
                    opportunity.website_structured_findings_json
                )

        except Exception:

            opportunity.website_structured_findings = []

        # --------------------------------------------------
        # IMPORTANT
        # Re-run processor to rebuild assessment
        # --------------------------------------------------

        opportunity = self.processor.process(
            opportunity
        )

        return {

            "id": row["id"],

            "opportunity": opportunity,

        }

    # --------------------------------------------------
    # Best Opportunity
    # --------------------------------------------------

    def get_best(self):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id

            FROM opportunities

            ORDER BY

                roi_score DESC,

                estimated_value DESC,

                opportunity_score DESC

            LIMIT 1
            """
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:

            return None

        return self.get_by_id(
            row[0]
        )

    # --------------------------------------------------
    # Latest
    # --------------------------------------------------

    def latest(self, limit=10):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id

            FROM opportunities

            ORDER BY created_at DESC

            LIMIT ?
            """,
            (limit,),
        )

        ids = [

            row[0]

            for row in cursor.fetchall()

        ]

        connection.close()

        return [

            self.get_by_id(i)

            for i in ids

        ]