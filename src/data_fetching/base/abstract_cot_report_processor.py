from abc import ABC, abstractmethod

import pandas as pd


class AbstractCotReportProcessor(ABC):

    @abstractmethod
    def process_report(
            self,
            cot_report_data: pd.DataFrame,
            columns_to_keep: dict,
            contracts_to_keep: list[str]
    ) ->pd.DataFrame:
        ...

    @staticmethod
    @abstractmethod
    def fetch_contract_reports(
            cot_report_data: pd.DataFrame,
            contract_name: str,
            periods_to_fetch: int
    ) -> pd.DataFrame:
        ...