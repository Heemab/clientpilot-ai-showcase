from dataclasses import dataclass, field

from src.models.audit_finding import AuditFinding


@dataclass(slots=True)
class AuditResult:
    """
    Result of one audit module.
    """

    name: str

    score: int = 100

    findings: list[AuditFinding] = field(default_factory=list)

    metrics: dict = field(default_factory=dict)

    def add(self, finding: AuditFinding):

        self.findings.append(finding)

    @property
    def issue_count(self):

        return len(self.findings)