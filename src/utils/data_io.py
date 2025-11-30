from pathlib import Path
from typing import Optional
import pandas as pd


def read_csv(path: Path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)


def write_csv(df: pd.DataFrame, path: Path, index: bool = False, **kwargs) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index, **kwargs)


def read_parquet(path: Path, **kwargs) -> pd.DataFrame:
    return pd.read_parquet(path, **kwargs)


def write_parquet(df: pd.DataFrame, path: Path, **kwargs) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, **kwargs)
