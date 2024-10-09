import logging


class Logger:

    def __init__(self, log_file: str, log_level: int = logging.INFO):
        self._log_file: str = log_file
        self._log_level: int = log_level
        self._logger: logging.Logger = logging.getLogger("Logger")
        self._configure_logger()

    def _configure_logger(self) -> None:
        self._logger.setLevel(self._log_level)

        formatter: logging.Formatter = logging.Formatter("'%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        file_handler: logging.FileHandler = logging.FileHandler(self._log_file)
        file_handler.setLevel(self._log_level)
        file_handler.setFormatter(formatter)

        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setLevel(self._log_level)
        console_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        return self._logger
