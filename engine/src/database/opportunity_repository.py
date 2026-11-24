from src.database.database import Database
from src.database.crm_repository import CRMRepository
from src.models.opportunity import Opportunity


class OpportunityRepository:
    """
    Handles saving and retrieving opportunities.
    """

    def __init__(self):

        self.db = Database()

        self.crm = CRMRepository()

    # --------------------------------------------------
    # Check if opportunity already exists
    # --------------------------------------------------

    def exists(self, opportunity: Opportunity):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id

            FROM opportunities

            WHERE website = ?
               OR phone = ?

            LIMIT 1
            """,
            (
                opportunity.website,
                opportunity.phone,
            ),
        )

        result = cursor.fetchone()

        connection.close()

        return result is not None

    # --------------------------------------------------
    # Save Opportunity
    # --------------------------------------------------

    def save(self, opportunity: Opportunity):

        if self.exists(opportunity):

            print(
                f"⚠ Skipped duplicate: {opportunity.business_name}"
            )

            return False

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO opportunities
            (

                source,

                business_name,

                category,

                address,

                phone,

                website,

                rating,

                reviews,

                opportunity_score,

                technology,

                priority,

                recommended_services,

                primary_service,

                estimated_value,

                estimated_hours,

                difficulty,

                closing_probability,

                roi_score,

                sales_reason,

                status,

                last_contacted,

                follow_up_date,

                notes,

                website_report_json,

                website_findings_json,

                website_structured_findings_json,

                business_email,

                contact_page,

                facebook_url,

                linkedin_url,

                instagram_url,

                owner_name

            )

            VALUES
            (

                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,

                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,

                ?, ?, ?, ?, ?, ?

            )
            """,
            (

                opportunity.source,

                opportunity.business_name,

                opportunity.category,

                opportunity.address,

                opportunity.phone,

                opportunity.website,

                opportunity.rating,

                opportunity.reviews,

                opportunity.opportunity_score,

                opportunity.technology,

                opportunity.priority,

                opportunity.recommended_services,

                opportunity.primary_service,

                opportunity.estimated_value,

                opportunity.estimated_hours,

                opportunity.difficulty,

                opportunity.closing_probability,

                opportunity.roi_score,

                opportunity.sales_reason,

                opportunity.status,

                opportunity.last_contacted,

                opportunity.follow_up_date,

                opportunity.notes,

                getattr(
                    opportunity,
                    "website_report_json",
                    "",
                ),

                getattr(
                    opportunity,
                    "website_findings_json",
                    "",
                ),

                getattr(
                    opportunity,
                    "website_structured_findings_json",
                    "",
                ),

                getattr(
                    opportunity,
                    "business_email",
                    "",
                ),

                getattr(
                    opportunity,
                    "contact_page",
                    "",
                ),

                getattr(
                    opportunity,
                    "facebook_url",
                    "",
                ),

                getattr(
                    opportunity,
                    "linkedin_url",
                    "",
                ),

                getattr(
                    opportunity,
                    "instagram_url",
                    "",
                ),

                getattr(
                    opportunity,
                    "owner_name",
                    "",
                ),

            ),
        )

        opportunity_id = cursor.lastrowid

        connection.commit()

        connection.close()

        self.crm.create(opportunity_id)

        print(
            f"✅ Saved: {opportunity.business_name}"
        )

        return opportunity_id