import json
import yaml
import csv
from pathlib import Path
from typing import List, Dict, Any


def load_yaml(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data if isinstance(data, list) else [data]


def load_json(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else [data]


def load_csv(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_test_data(file_name: str, data_dir: str = None) -> List[Dict[str, Any]]:
    if data_dir is None:
        data_dir = Path(__file__).parent / "test_data"
    else:
        data_dir = Path(data_dir)

    file_path = data_dir / file_name
    suffix = file_path.suffix.lower()

    loaders = {
        ".yaml": load_yaml,
        ".yml": load_yaml,
        ".json": load_json,
        ".csv": load_csv,
    }

    if suffix not in loaders:
        raise ValueError(f"Unsupported file type: {suffix}")

    return loaders[suffix](str(file_path))
