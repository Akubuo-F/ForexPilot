import yaml
import os
from root_directory_helper import RootDirectoryHelper


class ConfigLoader:

    @staticmethod
    def load_config(env: str) -> dict:
        root_dir: str = RootDirectoryHelper().root_dir
        config_path = os.path.join(root_dir, "config", f"{env}")
        with open(config_path, "r") as file:
            config: dict = yaml.safe_load(file)
        return config
