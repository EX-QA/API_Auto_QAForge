import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = Path(__file__).parent / "environments.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

    def get_env(self):
        env = os.getenv("ENV", self._config.get("default", "dev"))
        return self._config["environments"].get(env, self._config["environments"]["dev"])

    @property
    def base_url(self):
        return self.get_env()["base_url"]

    @property
    def timeout(self):
        return self.get_env()["timeout"]

    @property
    def verify_ssl(self):
        return self.get_env()["verify_ssl"]

    @property
    def pingcode_base_url(self):
        return self.get_env()["pingcode_base_url"]

    @property
    def pingcode_client_id(self):
        return os.getenv('PINGCODECLINETID')

    @property
    def pingcode_client_secret(self):
        return os.getenv('PINGCODECLINETSECRET')

    @property
    def pingcode_project_name(self):
        return self.get_env()["pingcode_project_name"]


def get_config():
    return Config()
