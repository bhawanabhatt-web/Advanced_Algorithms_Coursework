from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd

__all__ = [
    "PROJECT_ROOT",
    "RESULTS_DIR",
    "EXCEL_DIR",
    "PLOTS_DIR",
    "RAW_DATA_DIR",
    "ensure_dir",
    "get_logger",
    "export_to_csv",
]

# The project root is the parent of the `common` package itself, i.e. the
# directory that contains `common/`, `Task1/`, `Task2/`, ... and `results/`.
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
RESULTS_DIR: Path = PROJECT_ROOT / "results"
EXCEL_DIR: Path = RESULTS_DIR / "excel"
PLOTS_DIR: Path = RESULTS_DIR / "plots"
RAW_DATA_DIR: Path = RESULTS_DIR / "raw_data"


def ensure_dir(path: Path) -> Path:
   
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)-7s %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def export_to_csv(
    records: Iterable[Mapping[str, Any]], output_path: Path, index: bool = False
) -> Path:
    
    records_list = list(records)
    if not records_list:
        raise ValueError("Cannot export an empty collection of records to CSV.")

    ensure_dir(output_path.parent)
    frame = pd.DataFrame.from_records(records_list)
    frame.to_csv(output_path, index=index)
    return output_path