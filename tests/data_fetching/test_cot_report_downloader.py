import unittest
from datetime import datetime

import pandas as pd

from src.data_fetching.legacy_futures_cot_report_downloader import LegacyFuturesCotReportDownloader
from src.data_fetching.cot_report_processor import CotReportProcessor
from src.utils.config_loader import ConfigLoader
from src.utils.logger import Logger
from src.utils.root_directory_helper import RootDirectoryHelper


class TestCotReportDownloader(unittest.TestCase):

    def setUp(self):
        log_file_path: str = ConfigLoader.load_yaml_config("paths.yml")["logging"]["cot_report_downloader"]
        logger: Logger = Logger(
            log_file=f"{RootDirectoryHelper().root_dir}/{log_file_path}"
        )
        cot_report_processor: CotReportProcessor = CotReportProcessor()
        self.cot_downloader: LegacyFuturesCotReportDownloader = LegacyFuturesCotReportDownloader(cot_report_processor, logger)

    def test_download_report(self):
        report_years: list[int] = [2024]

        try:
            cot_report: pd.DataFrame = self.cot_downloader.download_report(report_years)

            self.assertIsInstance(cot_report, pd.DataFrame, "Output is not a DataFrame.")
            self.assertFalse(cot_report.empty, "DataFrame is empty.")

            csv_filepath: str = f"{RootDirectoryHelper().root_dir}/csv_files/cot_reports/tests/cot_report_downloader/cot_reports.csv"
            cot_report.to_csv(csv_filepath, sep=',', quotechar='"')

            print(f"Report Head\n: {cot_report.head()}")
            print(f"Report Tail\n: {cot_report.tail()}")
            print(f"Columns\n: {cot_report.columns}")
        except Exception as e:
            self.fail(f"Test failed with exception: {e}.")

    def test_download_report_as_school_year(self):
        current_year: int = datetime.today().year
        print(f"Current_year: {current_year}")

        try:
            expected_cot_report: pd.DataFrame = self.cot_downloader.download_report(
                [current_year - 1, current_year],
            )

            actual_cot_report: pd.DataFrame = self.cot_downloader.download_report_as_school_year(
                current_year,
            )
            self.assertEqual(
                len(actual_cot_report),
                len(expected_cot_report),
                "Actual Cot report is not equal to Expected Cot Report"
            )
        except Exception as e:
            self.fail(f"Test failed with exception: {e}.")




if __name__ == '__main__':
    unittest.main()
