import json
from pathlib import Path


class QueueState:
    """
    Stores the search queue progress.
    """

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        state_folder = project_root / "data" / "state"

        state_folder.mkdir(parents=True, exist_ok=True)

        self.state_file = state_folder / "queue_state.json"

        if not self.state_file.exists():

            self.save(
                {
                    "current_index": 0
                }
            )

    def load(self):

        with open(self.state_file, "r", encoding="utf-8") as file:

            return json.load(file)

    def save(self, state):

        with open(self.state_file, "w", encoding="utf-8") as file:

            json.dump(state, file, indent=4)