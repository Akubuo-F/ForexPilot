from datetime import datetime

import pandas as pd
import plotly.express as px

from src.data_fetching.cot_report_processor import CotReportProcessor
from src.lingos.confident_lingo import ConfidentLingo
from src.lingos.divergence_lingo import DivergenceLingo
from src.lingos.extreme_lingo import ExtremeLingo
from src.lingos.sentiment_lingo import SentimentLingo
from src.lingos.strength_lingo import StrengthLingo
from src.sentiment_analysis.cot_reports.base.abstract_cot_report_analyser import AbstractCotReportAnalyser
from src.sentiment_analysis.cot_reports.cot_report import CotReport
from src.utils.config_loader import ConfigLoader
from src.utils.root_directory_helper import RootDirectoryHelper


class CotReportAnalyser(AbstractCotReportAnalyser):

    def __init__(self, periods_to_analyse: int):
        self._periods_to_analyse: int = periods_to_analyse

    def get_reports_to_analyse(self, cot_reports) -> list[CotReport]:
        reports_to_analyse: list[CotReport] = cot_reports[-self._periods_to_analyse: ]
        return reports_to_analyse

    def analyse_sentiment(self, cot_reports: list[CotReport]) -> SentimentLingo:
        total_longs: int = 0
        total_shorts: int = 0
        total_spreading: int = 0
        for report in self.get_reports_to_analyse(cot_reports):
            total_longs += report.noncommercial_longs
            total_shorts += report.noncommercial_shorts
            total_spreading += report.noncommercial_spreading
        is_longs_greater: bool = total_longs > total_shorts + total_spreading
        is_shorts_greater: bool = total_shorts > total_longs + total_spreading
        if is_longs_greater:
            return SentimentLingo.BULLISH_SENTIMENT
        elif is_shorts_greater:
            return SentimentLingo.BEARISH_SENTIMENT
        else:
            return SentimentLingo.NEUTRAL

    def analyse_sentiment_strength(
            self, cot_reports: list[CotReport],
            weak_threshold: float,
            strong_threshold: float
    ) -> StrengthLingo:
        sentiment: SentimentLingo = self.analyse_sentiment(cot_reports)
        percentage_longs: float = 0
        percentage_shorts: float = 0
        for report in self.get_reports_to_analyse(cot_reports):
            percentage_longs += report.percentage_noncommercial_longs
            percentage_shorts += report.percentage_noncommercial_shorts
        if sentiment == SentimentLingo.BULLISH_SENTIMENT:
            return self._get_strength(percentage_longs, weak_threshold, strong_threshold)
        if sentiment == SentimentLingo.BEARISH_SENTIMENT:
            return self._get_strength(percentage_shorts, weak_threshold, strong_threshold)

    @staticmethod
    def _get_strength(percentage_value: float, weak_threshold: float, strong_threshold: float) -> StrengthLingo:
        if percentage_value >= strong_threshold:
            return StrengthLingo.STRONG
        elif percentage_value <= weak_threshold:
            return StrengthLingo.WEAK
        else:
            return StrengthLingo.NEUTRAL

    def analyse_confidence(self, cot_reports: list[CotReport]) -> ConfidentLingo:
        recent_report: CotReport = cot_reports[-1]
        recent_change_in_longs = recent_report.change_in_noncommercial_longs
        recent_change_in_shorts = recent_report.change_in_noncommercial_shorts
        recent_change_in_spreading = recent_report.change_in_noncommercial_spreading

        bullish_confident: bool = (
                recent_change_in_longs > 0 > recent_change_in_shorts and recent_change_in_spreading < 0
        )

        bearish_confident: bool = (
                recent_change_in_longs < 0 < recent_change_in_shorts and recent_change_in_spreading > 0
        )

        if bullish_confident:
            return ConfidentLingo.BULLISH_CONFIDENT
        elif bearish_confident:
            return ConfidentLingo.BEARISH_CONFIDENT
        else:
            return ConfidentLingo.NEUTRAL


    def analyse_divergence(self, cot_reports: list[CotReport]) -> DivergenceLingo:
        recent_report: CotReport = cot_reports[-1]
        historical_longs: int = 0
        historical_shorts: int = 0
        historical_spreading: int = 0
        for report in self.get_reports_to_analyse(cot_reports)[: -1]:
            historical_longs += report.noncommercial_longs
            historical_shorts += report.noncommercial_shorts
            historical_spreading += report.noncommercial_spreading
        historical_reports_length: int = len(cot_reports[: -1])
        historical_average_longs: float = historical_longs / historical_reports_length
        historical_average_shorts: float = historical_shorts / historical_reports_length
        historical_average_spreading: float = historical_spreading / historical_reports_length

        is_bearish_divergence: bool = (
            recent_report.noncommercial_longs > historical_average_longs and
            recent_report.noncommercial_shorts < historical_average_shorts and
            recent_report.noncommercial_spreading < historical_average_spreading
        )

        is_bullish_divergence: bool = (
            recent_report.noncommercial_longs < historical_average_longs and
            recent_report.noncommercial_shorts > historical_average_shorts and
            recent_report.noncommercial_spreading > historical_average_spreading
        )

        if is_bullish_divergence:
            return DivergenceLingo.BULLISH_DIVERGENCE
        elif is_bearish_divergence:
            return DivergenceLingo.BEARISH_DIVERGENCE
        else:
            return DivergenceLingo.NEUTRAL


    def analyse_extreme(self, cot_reports: list[CotReport], extreme_threshold: float) -> ExtremeLingo:
        recent_report: CotReport =  cot_reports[-1]
        historical_percentage_longs: float = 0.0
        historical_percentage_shorts: float = 0.0

        reports_to_analyse: list[CotReport] = self.get_reports_to_analyse(cot_reports)
        for report in reports_to_analyse:
            historical_percentage_longs += report.percentage_noncommercial_longs
            historical_percentage_shorts += report.percentage_noncommercial_shorts
        historical_report_length: int = len(reports_to_analyse)

        average_percentage_longs = historical_percentage_longs/historical_report_length
        average_percentage_shorts = historical_percentage_shorts/historical_report_length

        overbought_threshold: float = average_percentage_longs * (1 + (extreme_threshold/100))
        oversold_threshold: float = average_percentage_shorts * (1 + (extreme_threshold/100))

        is_overbought = recent_report.percentage_noncommercial_longs > overbought_threshold
        is_oversold = recent_report.percentage_noncommercial_shorts > oversold_threshold

        if is_overbought:
            return ExtremeLingo.OVERBOUGHT
        elif is_oversold:
            return ExtremeLingo.OVERSOLD
        else:
            return ExtremeLingo.NEUTRAL

    def plot_timeseries_of_noncommercial_net_positions(self, cot_reports: list[CotReport], show_spreading: bool = True) -> None:
        report_dates: list[datetime] = []
        net_positions: list[int] = []
        for report in self.get_reports_to_analyse(cot_reports):
            report_dates.append(pd.to_datetime(report.report_date))
            net_positions.append(report.net_position)

        constants: dict[str, str] = ConfigLoader.load_json_config("constants.json")["cot_report"]["columns_to_keep"]
        report_date_label: str = constants["As of Date in Form YYYY-MM-DD"].capitalize()
        net_position_label: str = "Net position"

        data = pd.DataFrame(
            {
                report_date_label: report_dates,
                net_position_label: net_positions
            }
        )
        fig = px.line(
            data,
            x=report_date_label,
            y=[net_position_label],
            labels={
                report_date_label: report_date_label,
                net_position_label: f"{net_position_label} (Longs - Shorts)"
            },
            title='Trend of Noncommercial Trader Sentiment (Bullishness/Bearishness)'
        )

        fig.show()
        fig.write_image("timeseries_plot.png")


if __name__ == '__main__':
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

    def main(plot_short_term: bool = False, plot_long_term: bool = False):
        cot_report_csv_file: str = ConfigLoader.load_yaml_config("paths.yml")["cot_report"]["test_csv_download"]
        cot_report_data = pd.read_csv(f"{RootDirectoryHelper().root_dir}/{cot_report_csv_file}")
        cot_reports = construct_cot_reports(cot_report_data, "GOLD - COMMODITY EXCHANGE INC.", 24)

        for report in cot_reports:
            print(report, end="\n")

        constants: dict[str, int] = ConfigLoader.load_json_config("constants.json")["cot_report"]

        print("\nShort term")
        short_term: int = constants["periods_to_analyse_short_term"]
        short_term_cot_report_analyser: CotReportAnalyser = CotReportAnalyser(short_term)
        print(short_term_cot_report_analyser.analyse_sentiment(cot_reports))
        print(short_term_cot_report_analyser.analyse_sentiment_strength(cot_reports, 30.0, 70.0))
        print(short_term_cot_report_analyser.analyse_confidence(cot_reports))
        print(short_term_cot_report_analyser.analyse_extreme(cot_reports, 70.0))
        print(short_term_cot_report_analyser.analyse_divergence(cot_reports))
        if plot_short_term:
            short_term_cot_report_analyser.plot_timeseries_of_noncommercial_net_positions(cot_reports)

        print("\nLong Term")
        long_term: int = constants["periods_to_analyse_long_term"]
        long_term_cot_report_analyser: CotReportAnalyser = CotReportAnalyser(long_term)
        print(long_term_cot_report_analyser.analyse_sentiment(cot_reports))
        print(long_term_cot_report_analyser.analyse_sentiment_strength(cot_reports, 30.0, 70.0))
        print(long_term_cot_report_analyser.analyse_confidence(cot_reports))
        print(long_term_cot_report_analyser.analyse_extreme(cot_reports, 70.0))
        print(long_term_cot_report_analyser.analyse_divergence(cot_reports))
        if plot_long_term:
            long_term_cot_report_analyser.plot_timeseries_of_noncommercial_net_positions(cot_reports)

    main()