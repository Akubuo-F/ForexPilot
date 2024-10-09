from abc import ABC
from typing import Final


class ReportingEnvironments(ABC):
    LEGACY_REPORT_FUTURES_ONLY: Final[str] = "legacy_fut"
    DISAGGREGATED_REPORT_FUTURES_ONLY: Final[str] = "disaggregated_fut"