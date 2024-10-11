from abc import ABC, abstractmethod

from src.lingos.confident_lingo import ConfidentLingo
from src.lingos.divergence_lingo import DivergenceLingo
from src.lingos.extreme_lingo import ExtremeLingo
from src.lingos.sentiment_lingo import SentimentLingo
from src.lingos.strength_lingo import StrengthLingo
from src.sentiment_analysis.cot_reports.cot_report import CotReport


class AbstractCotReportAnalyser(ABC):

    @abstractmethod
    def analyse_sentiment(self, cot_reports: list[CotReport]) -> SentimentLingo:
        ...

    @abstractmethod
    def analyse_sentiment_strength(
            self,
            cot_reports: list[CotReport],
            weak_threshold: float,
            strong_threshold: float
    ) -> StrengthLingo:
        ...

    @abstractmethod
    def analyse_confidence(self, cot_reports: list[CotReport]) -> ConfidentLingo:
        ...

    @abstractmethod
    def analyse_divergence(self, cot_reports: list[CotReport]) -> DivergenceLingo:
        ...

    @abstractmethod
    def analyse_extreme(self, cot_reports: list[CotReport], extreme_threshold: float) -> ExtremeLingo:
        ...

    @abstractmethod
    def plot_timeseries_of_noncommercial_net_positions(self, cot_reports: list[CotReport], show_spreading: bool = True) -> None:
        ...