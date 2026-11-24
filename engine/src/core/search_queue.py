import csv
from itertools import product
from pathlib import Path

from src.core.queue_state import QueueState


class SearchQueue:
    """
    Generates search jobs and remembers progress.
    """

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.data_folder = self.project_root / "data"

        self.cities_folder = self.data_folder / "cities"

        self.industries_file = self.data_folder / "industries.csv"

        self.jobs = []

        self.state = QueueState()

        self.current_index = self.state.load()["current_index"]

        self._build_queue()

    def load_industries(self):

        industries = []

        with open(self.industries_file, newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                industry = row["industry"].strip()

                if industry:
                    industries.append(industry)

        return industries

    def load_cities(self):

        cities = []

        for file in sorted(self.cities_folder.glob("*.csv")):

            country = file.stem.replace("_", " ").title()

            with open(file, newline="", encoding="utf-8") as csvfile:

                reader = csv.DictReader(csvfile)

                for row in reader:

                    city = row["city"].strip()

                    if city:

                        cities.append(
                            {
                                "country": country,
                                "city": city,
                            }
                        )

        return cities

    def _build_queue(self):

        industries = self.load_industries()

        cities = self.load_cities()

        self.jobs = []

        for city, industry in product(cities, industries):

            self.jobs.append(
                {
                    "country": city["country"],
                    "city": city["city"],
                    "industry": industry,
                }
            )

    def get_next_search(self):

        if not self.jobs:
            raise Exception("Search queue is empty.")

        return self.jobs[self.current_index]

    def mark_completed(self):

        self.current_index += 1

        if self.current_index >= len(self.jobs):

            self.current_index = 0

        self.state.save(
            {
                "current_index": self.current_index
            }
        )

    def total_jobs(self):

        return len(self.jobs)

    def current_position(self):

        return self.current_index + 1