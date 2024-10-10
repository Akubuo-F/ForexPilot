import logging
from typing import Iterable

import cot_reports
import pandas as pd

from src.data_fetching.base.abstract_cot_report_downloader import AbstractCotReportDownloader
from src.utils.logger import Logger


class CotReportDownloader(AbstractCotReportDownloader):

    def __init__(self, logger: Logger):
        self._logger: logging.Logger = logger.get_logger()

    def download_report(
            self,
            report_years: Iterable[int],
            reporting_environments: Iterable[str]
    ) -> pd.DataFrame:
        try:
            reports: pd.DataFrame = self._download(report_years, reporting_environments)
            self._logger.info(f"Cot reports downloaded successfully.")
            return reports
        except Exception as e:
            self._logger.error(f"Failed to download cot reports: {e}")
            raise

    def download_report_as_school_year(self, current_year: int, reporting_environments: Iterable[str]) -> pd.DataFrame:
        start_year: int = current_year - 1
        end_year: int = current_year
        report_years: range = range(start_year, end_year + 1)
        return self.download_report(report_years, reporting_environments)

    @staticmethod
    def _download(report_years: Iterable[int], reporting_environments: Iterable[str]) -> pd.DataFrame:
        reports_list: list[pd.DataFrame] = []
        for reporting_environment in reporting_environments:
            for year in report_years:
                report: pd.DataFrame = pd.DataFrame(
                    data=cot_reports.cot_year(
                        year=year,
                        cot_report_type=reporting_environment,
                        store_txt=False,
                        verbose=False)
                )
                reports_list.append(report)
        return pd.concat(reports_list, ignore_index=True)