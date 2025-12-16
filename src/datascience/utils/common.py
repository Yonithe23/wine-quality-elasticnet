import os
import yaml
import logging
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError


# ✅ Custom Exceptions (minimal)
class CommonUtilsError(Exception):
    """Base exception for common.py"""


class EmptyFileError(CommonUtilsError):
    """Raised when file exists but has no usable content."""


class FileReadError(CommonUtilsError):
    """Raised when reading/parsing fails."""


class FileWriteError(CommonUtilsError):
    """Raised when writing/saving fails."""


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)

            # ✅ handle empty yaml properly
            if content is None:
                raise EmptyFileError(f"yaml file is empty: {path_to_yaml}")

            logging.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)

    except BoxValueError as e:
        # ✅ configbox-specific problem
        raise FileReadError(f"Invalid YAML structure for ConfigBox: {path_to_yaml}") from e

    except EmptyFileError:
        raise

    except Exception as e:
        # ✅ any other read/parsing error
        raise FileReadError(f"Failed to read yaml file: {path_to_yaml}") from e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"json file saved at: {path}")

    except Exception as e:
        raise FileWriteError(f"Failed to save json: {path}") from e


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    try:
        with open(path) as f:
            content = json.load(f)

        # ✅ empty json file check (optional but useful)
        if content is None or content == {}:
            raise EmptyFileError(f"json file is empty: {path}")

        logging.info(f"json file loaded succesfully from: {path}")
        return ConfigBox(content)

    except EmptyFileError:
        raise

    except Exception as e:
        raise FileReadError(f"Failed to load json: {path}") from e


@ensure_annotations
def save_bin(data: Any, path: Path):
    try:
        joblib.dump(value=data, filename=path)
        logging.info(f"binary file saved at: {path}")
    except Exception as e:
        raise FileWriteError(f"Failed to save binary: {path}") from e


@ensure_annotations
def load_bin(path: Path) -> Any:
    try:
        data = joblib.load(path)
        logging.info(f"binary file loaded from: {path}")
        return data
    except Exception as e:
        raise FileReadError(f"Failed to load binary: {path}") from e
