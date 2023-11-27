# %%
import logging

import pandas as pd

from src.config import Config as cfg
from src.reuters_summary.step_1_generate_summaries import generate_summaries
from utils import save_parquet

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    df = pd.read_parquet(cfg.RAW_DATA_PATH)
    df_summarised = generate_summaries(df)

    logger.info(
        f"Saving df with {df_summarised.shape[0]} rows and {df_summarised.shape[1]} columns."
    )
    save_parquet(df=df_summarised, path=cfg.SUMMARISED_DATA_PATH, partition_col="date")
