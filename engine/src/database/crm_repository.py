from src.database.database import Database


class CRMRepository:
    """
    Handles CRM records for opportunities.
    """

    def __init__(self):
        self.db = Database()

    def create(self, opportunity_id):
        """
        Create a CRM record for a newly discovered opportunity.
        """

        connection = self.db.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO crm
            (
                opportunity_id
            )
            VALUES
            (
                ?
            )
            """,
            (opportunity_id,),
        )

        connection.commit()
        connection.close()

    def update_status(self, opportunity_id, status):

        connection = self.db.connect()
        cursor = connection.cursor()

        cursor.execute(
    """
    UPDATE crm

    SET
        status = ?,
        updated_at = CURRENT_TIMESTAMP

    WHERE opportunity_id = ?
    """,
    (
        status,
        opportunity_id,
    ),
)

        connection.commit()
        connection.close()

    def add_note(self, opportunity_id, note):

        connection = self.db.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE crm

            SET
                notes = ?

            WHERE opportunity_id = ?
            """,
            (
                note,
                opportunity_id,
            ),
        )

        connection.commit()
        connection.close()

    def schedule_follow_up(
        self,
        opportunity_id,
        follow_up_date,
    ):

        connection = self.db.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE crm

            SET
                follow_up_date = ?

            WHERE opportunity_id = ?
            """,
            (
                follow_up_date,
                opportunity_id,
            ),
        )

        connection.commit()
        connection.close()