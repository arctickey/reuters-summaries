# %%
import datetime
import logging
from dataclasses import asdict

import pandas as pd

from src.config import Config as cfg
from src.reuters_summary.step_0_scraper import scrape_articles
from src.utils import save_parquet

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    scraped_articles = scrape_articles(
        areas_to_fetch=cfg.WORLD_AREAS_TO_FETCH,
        reuters_url=cfg.REUTERS_URL,
        number_of_world_articles_to_fetch=cfg.NUMBER_OF_WORLD_ARTICLES_TO_FETCH,
        number_of_other_articles_to_fetch=cfg.NUMBER_OF_OTHER_ARTICLES_TO_FETCH,
    )
    df_to_save = pd.json_normalize(
        asdict(obj) for obj in scraped_articles
    )  # type: ignore
    df_to_save["date"] = int(datetime.date.today().strftime("%Y%m%d"))
    logger.info(
        f"Saving df with {df_to_save.shape[0]} rows and {df_to_save.shape[1]} columns."
    )
    save_parquet(df=df_to_save, path=cfg.RAW_DATA_PATH, partition_col="date")
# %%
