from datetime import datetime

from src.database.database import Database


class OutreachRepository:
    """
    Repository responsible for managing outreach
    packages.

    Responsibilities
    ----------------
    • Generate outreach numbers
    • Create outreach records
    • Retrieve outreach records
    • Update status
    • Update file paths
    """

    def __init__(self):

        self.db = Database()

    # --------------------------------------------------
    # Generate Outreach Number
    # --------------------------------------------------

    def generate_number(self):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM outreach
            """
        )

        count = cursor.fetchone()[0] + 1

        connection.close()

        year = datetime.now().year

        return f"OUT-{year}-{count:06d}"

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def create(
        self,
        opportunity_id,
    ):

        outreach_number = self.generate_number()

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO outreach
            (

                outreach_number,

                opportunity_id,

                status

            )

            VALUES

            (

                ?, ?, ?

            )
            """,
            (

                outreach_number,

                opportunity_id,

                "DRAFT",

            ),
        )

        outreach_id = cursor.lastrowid

        connection.commit()

        connection.close()

        return {

            "id": outreach_id,

            "outreach_number": outreach_number,

            "status": "DRAFT",

        }

    # --------------------------------------------------
    # Update Status
    # --------------------------------------------------

    def update_status(
        self,
        outreach_id,
        status,
    ):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE outreach

            SET

                status=?,

                updated_at=CURRENT_TIMESTAMP

            WHERE id=?
            """,
            (
                status,
                outreach_id,
            ),
        )

        connection.commit()

        connection.close()

    # --------------------------------------------------
    # Update Paths
    # --------------------------------------------------

    def update_paths(
        self,
        outreach_id,
        folder_path="",
        json_path="",
    ):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE outreach

            SET

                folder_path=?,

                json_path=?,

                updated_at=CURRENT_TIMESTAMP

            WHERE id=?
            """,
            (
                folder_path,
                json_path,
                outreach_id,
            ),
        )

        connection.commit()

        connection.close()

    # --------------------------------------------------
    # Get
    # --------------------------------------------------

    def get(
        self,
        outreach_id,
    ):

        connection = self.db.connect()

        connection.row_factory = lambda cursor, row: {

            cursor.description[idx][0]: row[idx]

            for idx in range(len(cursor.description))

        }

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM outreach

            WHERE id=?
            """,
            (
                outreach_id,
            ),
        )

        result = cursor.fetchone()

        connection.close()

        return result

    # --------------------------------------------------
    # Count
    # --------------------------------------------------

    def count(self):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM outreach
            """
        )

        total = cursor.fetchone()[0]

        connection.close()

        return total