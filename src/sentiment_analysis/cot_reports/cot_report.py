class CotReport:

    def __init__(
            self,
            contract_name: str,
            report_date: str,
            open_interest: int,
            noncommercial_longs: int,
            noncommercial_shorts: int,
            noncommercial_spreading: int,
            change_in_open_interest: int,
            change_in_noncommercial_longs: int,
            change_in_noncommercial_shorts: int,
            change_in_noncommercial_spreading: int
    ):
        self._contract_name: str = contract_name
        self._report_date: str = report_date
        self._open_interest: int = open_interest
        self._noncommercial_longs: int = noncommercial_longs
        self._noncommercial_shorts: int = noncommercial_shorts
        self._noncommercial_spreading: int = noncommercial_spreading
        self._change_in_open_interest: int = change_in_open_interest
        self._change_in_noncommercial_longs: int = change_in_noncommercial_longs
        self._change_in_noncommercial_shorts: int = change_in_noncommercial_shorts
        self._change_in_noncommercial_spreading: int = change_in_noncommercial_spreading

    def __repr__(self) -> str:
        contract_name: str = f"contract_name: {self._contract_name}"
        report_date: str = f"report_date: {self._report_date}"
        open_interest: str = f"open_interest: {self._open_interest}"
        noncommercial_longs: str = f"noncommercial_longs: {self._noncommercial_longs}"
        noncommercial_shorts: str = f"noncommercial_shorts: {self._noncommercial_shorts}"
        noncommercial_spreading: str = f"noncommercial_spreading: {self._noncommercial_spreading}"
        change_in_open_interest: str = f"change_in_open_interest: {self._change_in_open_interest}"
        change_in_noncommercial_longs: str = f"change_in_noncommercial_longs: {self._change_in_noncommercial_longs}"
        change_in_noncommercial_shorts: str = f"change_in_noncommercial_shorts: {self._change_in_noncommercial_shorts}"
        change_in_noncommercial_spreading: str = f"change_in_noncommercial_spreading: {self._change_in_noncommercial_spreading}"
        percentage_noncommercial_longs: str = f"percentage_noncommercial_longs: {self.percentage_noncommercial_longs}"
        percentage_noncommercial_shorts: str = f"percentage_noncommercial_shorts: {self.percentage_noncommercial_shorts}"
        percentage_noncommercial_spreading: str = f"percentage_noncommercial_spreading: {self.percentage_noncommercial_spreading}"
        total_noncommercial_position: str = f"total_noncommercial_position: {self.total_noncommercial_positions}"
        net_position: str = f"net_position: {self.net_position}"
        return ", ".join([
            contract_name,
            report_date,
            open_interest,
            noncommercial_longs,
            noncommercial_shorts,
            noncommercial_spreading,
            change_in_open_interest,
            change_in_noncommercial_longs,
            change_in_noncommercial_shorts,
            change_in_noncommercial_spreading,
            percentage_noncommercial_longs,
            percentage_noncommercial_shorts,
            percentage_noncommercial_spreading,
            total_noncommercial_position,
            net_position
        ])

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def contract_name(self) -> str:
        return self._contract_name

    @property
    def report_date(self) -> str:
        return self._report_date

    @property
    def open_interest(self) -> int:
        return self._open_interest

    @property
    def noncommercial_longs(self) -> int:
        return self._noncommercial_longs

    @property
    def noncommercial_shorts(self) -> int:
        return self._noncommercial_shorts

    @property
    def noncommercial_spreading(self) -> int:
        return self._noncommercial_spreading

    @property
    def change_in_open_interest(self) -> int:
        return self._change_in_open_interest

    @property
    def change_in_noncommercial_longs(self) -> int:
        return self._change_in_noncommercial_longs

    @property
    def change_in_noncommercial_shorts(self) -> int:
        return self._change_in_noncommercial_shorts

    @property
    def change_in_noncommercial_spreading(self) -> int:
        return self._change_in_noncommercial_spreading

    @property
    def percentage_noncommercial_longs(self) -> float:
        longs: int = self._noncommercial_longs
        total_non_commercial_positions: int = self.total_noncommercial_positions
        percentage_longs: float = (longs/total_non_commercial_positions) * 100
        rounded_percentage_longs = round(percentage_longs, 2)
        return rounded_percentage_longs

    @property
    def percentage_noncommercial_shorts(self) -> float:
        shorts: int = self._noncommercial_shorts
        total_non_commercial_positions: int = self.total_noncommercial_positions
        percentage_shorts: float = (shorts / total_non_commercial_positions) * 100
        rounded_percentage_shorts = round(percentage_shorts, 2)
        return rounded_percentage_shorts

    @property
    def percentage_noncommercial_spreading(self) -> float:
        spreading: int = self._noncommercial_spreading
        total_non_commercial_positions: int = self.total_noncommercial_positions
        percentage_spreading: float = (spreading / total_non_commercial_positions) * 100
        rounded_percentage_spreading = round(percentage_spreading, 2)
        return rounded_percentage_spreading

    @property
    def total_noncommercial_positions(self) -> int:
        longs: int = self._noncommercial_longs
        shorts: int = self._noncommercial_shorts
        spreading: int = self._noncommercial_spreading
        positions: list[int] = [longs, shorts, spreading]
        return sum(positions)

    @property
    def net_position(self) -> int:
        return self._noncommercial_longs - self._noncommercial_shorts