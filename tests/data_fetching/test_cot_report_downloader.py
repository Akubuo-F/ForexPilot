import unittest

import pandas as pd

from src.data_fetching.cot_report_downloader.cot_report_downloader import CotReportDownloader
from src.data_fetching.cot_report_downloader.reporting_environments import ReportingEnvironments
from src.utils.logger import Logger
from src.utils.root_directory_helper import RootDirectoryHelper


class TestCotReportDownloader(unittest.TestCase):

    def setUp(self):
        logger: Logger = Logger(
            log_file=f"{RootDirectoryHelper().root_dir}/logs/data_fetching/tests/cot_report_downloader.log"
        )
        self.cot_downloader: CotReportDownloader = CotReportDownloader(logger)

    def test_download_report(self):
        report_years: list[int] = [2024]
        reporting_environments: list[str] = [
            ReportingEnvironments.LEGACY_REPORT_FUTURES_ONLY,
            ReportingEnvironments.DISAGGREGATED_REPORT_FUTURES_ONLY
        ]

        try:
            cot_report: pd.DataFrame = self.cot_downloader.download_report(report_years, reporting_environments)

            self.assertIsInstance(cot_report, pd.DataFrame, "Output is not a DataFrame.")
            self.assertFalse(cot_report.empty, "DataFrame is empty.")

            print(f"Report Head\n: {cot_report.head()}")
            print(f"Report Tail\n: {cot_report.tail()}")
        except Exception as e:
            self.fail(f"Test failed with exception: {e}.")


if __name__ == '__main__':
    unittest.main()
