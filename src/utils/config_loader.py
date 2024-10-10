import json

import yaml
import os

from src.utils.root_directory_helper import RootDirectoryHelper


class ConfigLoader:

    @staticmethod
    def load_yaml_config(env: str) -> dict:
        config_path: str = ConfigLoader._get_env_path(env)
        with open(config_path, "r") as config_file:
            config: dict = yaml.safe_load(config_file)
        return config

    @staticmethod
    def load_json_config(env) -> dict:
        config_path: str = ConfigLoader._get_env_path(env)
        with open(config_path, "r") as config_file:
            config: dict = json.load(config_file)
            return config

    @staticmethod
    def _get_env_path(env: str) -> str:
        root_dir: str = RootDirectoryHelper().root_dir
        return os.path.join(root_dir, "config", f"{env}")
