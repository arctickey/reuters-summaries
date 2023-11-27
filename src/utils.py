from pathlib import Path

import pandas as pd


def save_parquet(df: pd.DataFrame, path: Path, partition_col: str) -> None:
    if path.exists():
        if_append = True
    else:
        if_append = False
    df.to_parquet(path, partition_cols=partition_col, append=if_append)
