import os


class RootDirectoryHelper:
    def __init__(self):
        self._root_dir: str = self._find_root_directory()

    @staticmethod
    def _find_root_directory() -> str:
        """
        This method assumes the root directory contains a unique identifier config folder,
        which will act as a unique identifier for the r
        :return: str
        """
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        while current_dir != os.path.dirname(current_dir):
            if os.path.exists(os.path.join(current_dir, "config")):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        raise FileNotFoundError("Root directory containing 'config' not found.")

    @property
    def root_dir(self) -> str:
        return self._root_dir