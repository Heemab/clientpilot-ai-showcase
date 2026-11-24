from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.database.database import Database


class OpportunityExplorer:
    """
    Displays dashboard and opportunities stored
    in the database.
    """

    def __init__(self):

        self.db = Database()

        self.console = Console()

    # --------------------------------------------------
    # Sales Dashboard
    # --------------------------------------------------

    def show_dashboard(self):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM opportunities"
        )
        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM opportunities WHERE status='NEW'"
        )
        new = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM opportunities WHERE priority='HIGH'"
        )
        high = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM opportunities WHERE priority='MEDIUM'"
        )
        medium = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM opportunities WHERE priority='LOW'"
        )
        low = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM opportunities WHERE status='CONTACTED'"
        )
        contacted = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM opportunities WHERE status='CLIENT'"
        )
        clients = cursor.fetchone()[0]

        connection.close()

        dashboard = f"""
Total Leads        : {total}

New Leads          : {new}

High Priority      : {high}

Medium Priority    : {medium}

Low Priority       : {low}

Contacted          : {contacted}

Clients            : {clients}
"""

        self.console.print(
            Panel.fit(
                dashboard,
                title="TODAY'S SALES DASHBOARD",
                border_style="green",
            )
        )

    # --------------------------------------------------
    # Top Opportunities
    # --------------------------------------------------

    def show_top(self, limit=10):

        connection = self.db.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT

                business_name,

                technology,

                priority,

                rating,

                reviews,

                opportunity_score,

                recommended_services,

                status

            FROM opportunities

            ORDER BY

                opportunity_score DESC,

                rating DESC,

                reviews DESC

            LIMIT ?

            """,
            (limit,),
        )

        rows = cursor.fetchall()

        connection.close()

        table = Table(title="TOP HIGH VALUE OPPORTUNITIES")

        table.add_column("Business", style="cyan", width=30)

        table.add_column("Tech", style="green", width=14)

        table.add_column("Priority", style="red", width=10)

        table.add_column("Rating", justify="center")

        table.add_column("Reviews", justify="right")

        table.add_column("Score", style="yellow", justify="center")

        table.add_column("Best Service", style="magenta", width=28)

        table.add_column("Status", style="blue", width=10)

        for row in rows:

            service = ""

            if row[6]:
                service = row[6].split(",")[0].strip()

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5]),
                service,
                str(row[7]),
            )

        self.console.print(table)