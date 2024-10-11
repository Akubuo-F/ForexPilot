import pandas as pd

from src.data_fetching.base.abstract_cot_report_processor import AbstractCotReportProcessor


class CotReportProcessor(AbstractCotReportProcessor):

    def process_report(
            self,
            cot_report_data: pd.DataFrame,
            columns_to_keep: dict,
            contracts_to_keep: list[str]
    ) -> pd.DataFrame:
        processed_cot_report_data: pd.DataFrame = cot_report_data[columns_to_keep.keys()]
        processed_cot_report_data = processed_cot_report_data[
            processed_cot_report_data["Market and Exchange Names"].isin(contracts_to_keep)
        ]
        processed_cot_report_data = processed_cot_report_data.rename(columns=columns_to_keep)
        return processed_cot_report_data

    @staticmethod
    def fetch_contract_reports(
            cot_report_data: pd.DataFrame,
            contract_name: str,
            periods_to_fetch: int
    ) -> pd.DataFrame:
        filtered_reports = cot_report_data[cot_report_data['contract name'] == contract_name]
        return filtered_reports.head(periods_to_fetch)