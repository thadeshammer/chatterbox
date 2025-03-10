import logging.config
import os
from typing import Union

import yaml

from chatterbox_backend.config import Config


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.module = record.module
        record.funcName = record.funcName
        return super().format(record)


_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s::%(funcName)s - %(message)s"


def _extract_filenames_from_logger_config(logger_config: dict) -> list:
    filenames = []

    for handler in logger_config.get("handlers", {}).values():
        if "filename" in handler:
            filenames.append(handler["filename"])

    return filenames


def setup_logging(log_cfg_yaml_filepath: str) -> None:
    if os.path.exists(log_cfg_yaml_filepath):
        with open(log_cfg_yaml_filepath, "rt", encoding="UTF8") as config_file:
            config: Union[list, dict, None] = yaml.safe_load(config_file.read())
            if not isinstance(config, dict):
                raise TypeError(f"logging config is {type(config)} but needs be dict.")
            try:
                logging.config.dictConfig(config)
            except Exception as e:
                print(
                    f"Found but failed to load config from {log_cfg_yaml_filepath}: {str(e)}"
                )
                raise

            log_files: list = _extract_filenames_from_logger_config(config)

            print(f"Log file(s) are at: {log_files}", flush=True)
            return

    print("Log config not found, using defaults.", flush=True)
    logging.basicConfig(level=logging.DEBUG)

    # Create a custom formatter with the desired format
    custom_formatter = CustomFormatter(_LOG_FORMAT)

    # Add the custom formatter to all handlers
    for handler in logging.getLogger().handlers:
        handler.setFormatter(custom_formatter)
