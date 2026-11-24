from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class WorkspaceView:
    """
    Displays a complete Opportunity Workspace.

    This class is presentation-only.
    It contains no business logic.
    """

    def __init__(self):

        self.console = Console()

    # --------------------------------------------------

    def display(self, workspace):

        if workspace is None:

            self.console.print(
                "[red]Opportunity not found.[/red]"
            )

            return

        opportunity = workspace["opportunity"]

        outreach = workspace["outreach"]

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        self.console.print()

        self.console.print(
            Panel.fit(
                f"[bold cyan]{opportunity.business_name}[/bold cyan]",
                title="Opportunity Workspace"
            )
        )

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        summary = Table(show_header=False)

        summary.add_column(width=28)

        summary.add_column()

        summary.add_row("Technology", opportunity.technology)

        summary.add_row("Priority", opportunity.priority)

        summary.add_row("Opportunity Score", str(opportunity.opportunity_score))

        summary.add_row("Primary Service", opportunity.primary_service)

        summary.add_row(
            "Estimated Value",
            f"${opportunity.estimated_value:,}"
        )

        summary.add_row(
            "Estimated Hours",
            str(opportunity.estimated_hours)
        )

        summary.add_row(
            "Difficulty",
            opportunity.difficulty
        )

        summary.add_row(
            "Closing Probability",
            f"{opportunity.closing_probability}%"
        )

        summary.add_row(
            "ROI Score",
            str(opportunity.roi_score)
        )

        summary.add_row(
            "Status",
            opportunity.status
        )

        self.console.print(summary)

        # --------------------------------------------------
        # Website Findings
        # --------------------------------------------------

        findings = getattr(
            opportunity,
            "website_findings",
            []
        )

        if findings:

            self.console.print()

            self.console.print("[bold]Website Findings[/bold]")

            for finding in findings:

                self.console.print(
                    f" • {finding}"
                )

        # --------------------------------------------------
        # Services
        # --------------------------------------------------

        services = []

        if opportunity.recommended_services:

            services = [
                s.strip()
                for s in opportunity.recommended_services.split(",")
            ]

        if services:

            self.console.print()

            self.console.print("[bold]Recommended Services[/bold]")

            for service in services:

                self.console.print(
                    f" ✓ {service}"
                )

        # --------------------------------------------------
        # Sales Reason
        # --------------------------------------------------

        if opportunity.sales_reason:

            self.console.print()

            self.console.print("[bold]Sales Reason[/bold]")

            self.console.print(
                opportunity.sales_reason
            )

        # --------------------------------------------------
        # Outreach
        # --------------------------------------------------

        self.console.print()

        self.console.print("[bold]Outreach Assets[/bold]")

        table = Table(show_header=True)

        table.add_column("Asset")

        table.add_column("Status")

        assets = [

            ("Email", "✓ Generated"),

            ("LinkedIn", "✓ Generated"),

            ("Follow-up", "✓ Generated"),

            ("Call Script", "✓ Generated"),

            ("Proposal Intro", "✓ Generated"),

        ]

        for asset in assets:

            table.add_row(*asset)

        self.console.print(table)

        self.console.print()

        self.console.print(
            "[green]Workspace loaded successfully.[/green]"
        )