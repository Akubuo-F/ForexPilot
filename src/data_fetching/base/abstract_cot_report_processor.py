from abc import ABC, abstractmethod

import pandas as pd


class AbstractCotReportProcessor(ABC):

    @abstractmethod
    def process(self, cot_data: pd.DataFrame) ->pd.DataFrame:
        """
        Process the COT data and return a DataFrame with the required analysis.

        :param cot_data: DataFrame containing raw COT data
        :return: DataFrame with processed data
        """
        ...