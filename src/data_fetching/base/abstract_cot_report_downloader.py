from abc import ABC, abstractmethod
from typing import Iterable

import pandas as pd


class AbstractCotReportDownloader(ABC):

    @abstractmethod
    def download_report(
            self,
            report_years: Iterable[int],
            reporting_environments: Iterable[str]
    ) -> pd.DataFrame:
        ...

    @abstractmethod
    def download_report_as_school_year(
            self,
            current_year: int,
            reporting_environments: Iterable[str]
    ) -> pd.DataFrame:
        ...