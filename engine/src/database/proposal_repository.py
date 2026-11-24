from datetime import datetime

from src.database.database import Database


class ProposalRepository:
    """
    Repository responsible for managing proposals.

    Responsibilities
    ----------------
    • Generate proposal numbers
    • Create proposal records
    • Retrieve proposal records
    • Update proposal status
    """

    def __init__(self):

        self.db = Database()

    # --------------------------------------------------
    # Generate Proposal Number
    # --------------------------------------------------

    def generate_number(self):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM proposals
            """
        )

        count = cursor.fetchone()[0] + 1

        connection.close()

        year = datetime.now().year

        return f"PROP-{year}-{count:06d}"

    # --------------------------------------------------
    # Create Proposal
    # --------------------------------------------------

    def create(
        self,
        opportunity_id,
        markdown_path="",
        pdf_path="",
    ):

        proposal_number = self.generate_number()

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO proposals
            (

                proposal_number,

                opportunity_id,

                status,

                markdown_path,

                pdf_path

            )

            VALUES
            (

                ?, ?, ?, ?, ?

            )
            """,
            (

                proposal_number,

                opportunity_id,

                "DRAFT",

                markdown_path,

                pdf_path,

            ),
        )

        proposal_id = cursor.lastrowid

        connection.commit()

        connection.close()

        return {

            "id": proposal_id,

            "proposal_number": proposal_number,

            "status": "DRAFT",

        }

    # --------------------------------------------------
    # Get Proposal
    # --------------------------------------------------

    def get(self, proposal_id):

        connection = self.db.connect()

        connection.row_factory = lambda cursor, row: {

            cursor.description[idx][0]: row[idx]

            for idx in range(len(cursor.description))

        }

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM proposals

            WHERE id = ?
            """,
            (proposal_id,),
        )

        proposal = cursor.fetchone()

        connection.close()

        return proposal

    # --------------------------------------------------
    # Update Status
    # --------------------------------------------------

    def update_status(
        self,
        proposal_id,
        status,
    ):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE proposals

            SET

                status = ?,

                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                status,
                proposal_id,
            ),
        )

        connection.commit()

        connection.close()

        # --------------------------------------------------
    # Count
    # --------------------------------------------------

    def count(self):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM proposals
            """
        )

        total = cursor.fetchone()[0]

        connection.close()

        return total

    # --------------------------------------------------
    # Update File Paths
    # --------------------------------------------------

    def update_paths(
        self,
        proposal_id,
        markdown_path="",
        pdf_path="",
    ):
        """
        Update exported file locations.
        """

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE proposals

            SET

                markdown_path = ?,

                pdf_path = ?,

                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                markdown_path,
                pdf_path,
                proposal_id,
            ),
        )

        connection.commit()

        connection.close()