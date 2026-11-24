from src.core.search_queue import SearchQueue
from src.services.google_maps_service import GoogleMapsService
from src.normalizers.google_maps_normalizer import GoogleMapsNormalizer
from src.services.opportunity_processor import OpportunityProcessor
from src.database.opportunity_repository import OpportunityRepository
from src.services.opportunity_explorer import OpportunityExplorer
from src.services.client_workflow import ClientWorkflow


class Application:
    """
    Main application controller.

    Pipeline

        Search Queue
              ↓
        Google Maps
              ↓
        Normalize
              ↓
        Opportunity Analysis
              ↓
        Save Opportunity
              ↓
        Generate Proposal
              ↓
        Generate Outreach
              ↓
        Dashboard
    """

    def __init__(self):

        self.queue = SearchQueue()

        self.google_maps = GoogleMapsService()

        self.normalizer = GoogleMapsNormalizer()

        self.processor = OpportunityProcessor()

        self.repository = OpportunityRepository()

        self.explorer = OpportunityExplorer()

        self.workflow = ClientWorkflow()

    # --------------------------------------------------
    # Main
    # --------------------------------------------------

    def run(self):

        search = self.queue.get_next_search()

        print(
            f"Total Search Jobs: {self.queue.total_jobs()}"
        )

        query = search["industry"]

        location = (
            f"{search['city']}, "
            f"{search['country']}"
        )

        print("=" * 60)
        print("AI CLIENT ACQUISITION ENGINE")
        print("=" * 60)

        print(f"Industry : {query}")
        print(f"Location : {location}")

        print(
            f"Queue Position : "
            f"{self.queue.current_index}/"
            f"{self.queue.total_jobs()}"
        )

        print("\nSearching Google Maps...\n")

        businesses = self.google_maps.search(

            query=query,

            location=location,

        )

        print(
            f"Found {len(businesses)} businesses.\n"
        )

        saved = 0

        # --------------------------------------------------
        # Process Every Business
        # --------------------------------------------------

        for business in businesses:

            try:

                # ------------------------------
                # Normalize
                # ------------------------------

                opportunity = (
                    self.normalizer.normalize(
                        business
                    )
                )

                # ------------------------------
                # Analyze
                # ------------------------------

                opportunity = (
                    self.processor.process(
                        opportunity
                    )
                )

                # ------------------------------
                # Save
                # ------------------------------

                opportunity_id = (
                    self.repository.save(
                        opportunity
                    )
                )

                if not opportunity_id:

                    # Duplicate
                    continue

                saved += 1

                self.queue.mark_completed()

                # ------------------------------
                # Client Workflow
                # ------------------------------

                print(
                    f"Running workflow for "
                    f"Opportunity ID: "
                    f"{opportunity_id}"
                )

                try:

                    self.workflow.run(
                        opportunity_id
                    )

                except Exception as workflow_error:

                    print(

                        "Workflow warning:",

                        workflow_error,

                    )

            except Exception as processing_error:

                print()

                print(
                    "Processing Error:"
                )

                print(processing_error)

                print()

                # Continue with next business
                continue

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        print()

        print("=" * 60)

        print(
            f"Successfully saved "
            f"{saved} new opportunities."
        )

        print("=" * 60)

        # --------------------------------------------------
        # Dashboard
        # --------------------------------------------------

        print()

        self.explorer.show_dashboard()

        print()

        self.explorer.show_top(10)