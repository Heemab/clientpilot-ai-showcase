from pathlib import Path


class ProposalExporter:
    """
    Exports proposal documents.

    This class only writes files to disk.

    It does NOT decide where files should be stored.
    That responsibility belongs to ProposalPackage.
    """

    def __init__(self):
        pass

    # --------------------------------------------------
    # Export Markdown
    # --------------------------------------------------

    def export_markdown(
        self,
        markdown,
        output_path,
    ):
        """
        Save Markdown to the specified path.
        """

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(markdown)

        return output_path