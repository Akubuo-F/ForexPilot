from abc import ABC, abstractmethod

import pandas as pd


class AbstractCotReportProcessor(ABC):

    @abstractmethod
    def process_report(self, cot_report_data: pd.DataFrame, columns_to_keep: dict, contracts_to_keep: list[str]) ->pd.DataFrame:
        ...