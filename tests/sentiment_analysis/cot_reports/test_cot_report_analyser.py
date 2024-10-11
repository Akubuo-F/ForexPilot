import unittest

import pandas as pd

from src.data_fetching.cot_report_processor import CotReportProcessor
from src.lingos.confident_lingo import ConfidentLingo
from src.lingos.divergence_lingo import DivergenceLingo
from src.lingos.extreme_lingo import ExtremeLingo
from src.lingos.sentiment_lingo import SentimentLingo
from src.lingos.strength_lingo import StrengthLingo
from src.sentiment_analysis.cot_reports.cot_report import CotReport
from src.sentiment_analysis.cot_reports.cot_report_analyser import CotReportAnalyser
from src.utils.config_loader import ConfigLoader
from src.utils.root_directory_helper import RootDirectoryHelper


def construct_cot_reports(
        cot_report_data: pd.DataFrame,
        contract_to_construct: str,
        length_of_report: int
) -> list[CotReport]:
    cot_reports: pd.DataFrame = CotReportProcessor.fetch_contract_reports(
        cot_report_data,
        contract_to_construct,
        length_of_report
    )
    output: list[CotReport] = []
    for _, row in cot_reports.iterrows():
        cot_report: CotReport = CotReport(
            contract_name=row['contract name'],
            report_date=row['report date'],
            open_interest=row['open interest'],
            noncommercial_longs=row['noncommercial longs'],
            noncommercial_shorts=row['noncommercial shorts'],
            noncommercial_spreading=row['noncommercial spreading'],
            change_in_open_interest=row['open interests change'],
            change_in_noncommercial_longs=row['noncommercial longs change'],
            change_in_noncommercial_shorts=row['noncommercial shorts change'],
            change_in_noncommercial_spreading=row['noncommercial spreading change']
        )
        output.insert(0, cot_report)
    return output


class ConfidenceLingo:
    pass


class TestCotReportAnalyser(unittest.TestCase):

    def setUp(self):
        constants: dict[str, int] = ConfigLoader.load_json_config("constants.json")["cot_report"]
        short_term: int = constants["periods_to_analyse_short_term"]
        long_term: int = constants["periods_to_analyse_long_term"]
        self._short_term_cot_report_analyser: CotReportAnalyser = CotReportAnalyser(short_term)
        self._long_term_cot_report_analyser: CotReportAnalyser = CotReportAnalyser(long_term)

        mock_cot_report_csv_file: str = ConfigLoader.load_yaml_config("paths.yml")["cot_report"]["mock_cot_report"]
        cot_report_data = pd.read_csv(f"{RootDirectoryHelper().root_dir}/{mock_cot_report_csv_file}")
        self.cot_reports = construct_cot_reports(cot_report_data, "GOLD - COMMODITY EXCHANGE INC.", 24)

    def test_analyse_sentiment(self):
        expected_sentiment: SentimentLingo = SentimentLingo.BULLISH_SENTIMENT
        actual_sentiment: SentimentLingo = self._short_term_cot_report_analyser.analyse_sentiment(self.cot_reports)
        self.assertEqual(expected_sentiment, actual_sentiment)

    def test_analyse_sentiment_strength(self):
        weak_threshold = 30.0
        strong_threshold = 70.0
        expected_strength: StrengthLingo = StrengthLingo.STRONG
        actual_strength: StrengthLingo = self._short_term_cot_report_analyser.analyse_sentiment_strength(
            self.cot_reports, weak_threshold,
            strong_threshold
        )
        self.assertEqual(expected_strength, actual_strength)

    def test_analyse_confidence(self):
        expected_confidence: ConfidentLingo = ConfidentLingo.NEUTRAL
        actual_confidence: ConfidentLingo = self._short_term_cot_report_analyser.analyse_confidence(self.cot_reports)
        self.assertEqual(expected_confidence, actual_confidence)

    def test_analyse_divergence(self):
        expected_divergence: DivergenceLingo = DivergenceLingo.NEUTRAL
        actual_divergence: DivergenceLingo = self._short_term_cot_report_analyser.analyse_divergence(self.cot_reports)
        self.assertEqual(expected_divergence, actual_divergence)

    def test_analyse_extreme(self):
        extreme_threshold = 70.0
        expected_extreme: ExtremeLingo = ExtremeLingo.NEUTRAL
        actual_extreme: ExtremeLingo = self._short_term_cot_report_analyser.analyse_extreme(self.cot_reports, extreme_threshold)
        self.assertEqual(expected_extreme, actual_extreme)


if __name__ == '__main__':
    unittest.main()
