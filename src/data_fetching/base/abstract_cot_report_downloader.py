from abc import ABC, abstractmethod
from typing import Iterable

import pandas as pd


class AbstractCotReportDownloader(ABC):

    @abstractmethod
    def download_report(self, report_years: Iterable[int]) -> pd.DataFrame:
        ...

    @abstractmethod
    def download_report_as_school_year(self, current_year: int) -> pd.DataFrame:
        ...