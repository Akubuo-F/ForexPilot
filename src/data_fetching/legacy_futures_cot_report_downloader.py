import logging
from typing import Iterable, Final, Any

import cot_reports
import pandas as pd

from src.data_fetching.base.abstract_cot_report_downloader import AbstractCotReportDownloader
from src.data_fetching.cot_report_processor import CotReportProcessor
from src.utils.config_loader import ConfigLoader
from src.utils.logger import Logger


class LegacyFuturesCotReportDownloader(AbstractCotReportDownloader):
    REPORTING_ENVIRONMENT: Final[str] = "legacy_fut"

    def __init__(self, cot_report_processor: CotReportProcessor, logger: Logger):
        self._cot_report_processor: CotReportProcessor = cot_report_processor
        self._logger: logging.Logger = logger.get_logger()

    def download_report(
            self,
            report_years: Iterable[int],
    ) -> pd.DataFrame:
        try:
            reports: pd.DataFrame = self._download(report_years)
            self._logger.info(f"Cot reports downloaded successfully.")
            return reports
        except Exception as e:
            self._logger.error(f"Failed to download cot reports: {e}")
            raise

    def download_report_as_school_year(self, current_year: int) -> pd.DataFrame:
        start_year: int = current_year - 1
        end_year: int = current_year
        report_years: range = range(start_year, end_year + 1)
        return self.download_report(report_years)

    def _download(self, report_years: Iterable[int]) -> pd.DataFrame:
        reports_list: list[pd.DataFrame] = []
        for year in report_years:
            report: pd.DataFrame = pd.DataFrame(
                data=cot_reports.cot_year(
                    year=year,
                    cot_report_type=LegacyFuturesCotReportDownloader.REPORTING_ENVIRONMENT,
                    store_txt=False,
                    verbose=False)
            )

            cot_report_constants: dict[str, Any] = ConfigLoader.load_json_config("constants.json")["cot_report"]
            columns_to_keep: dict = cot_report_constants["columns_to_keep"]
            contracts_to_keep: list[str] = cot_report_constants["contracts_to_keep"]
            processed_report: pd.DataFrame = self._cot_report_processor.process_report(
                cot_report_data=report,
                columns_to_keep=columns_to_keep,
                contracts_to_keep=contracts_to_keep,
            )
            reports_list.append(processed_report)
        return pd.concat(reports_list, ignore_index=True)