# %%
import logging

from src.config import Config as cfg
from src.reuters_summary.step_0_scraper import scrape_articles
from src.utils import save_parquet

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    scraped_articles = scrape_articles(
        areas_to_fetch=cfg.WORLD_AREAS_TO_FETCH,
        reuters_url=cfg.REUTERS_URL,
        number_articles_to_fetch=cfg.NUMBER_ARTICLES_TO_FETCH,
    )
    logger.info(
        f"Saving df with {scraped_articles.shape[0]} rows and {scraped_articles.shape[1]} columns."
    )
    save_parquet(df=scraped_articles, path=cfg.RAW_DATA_PATH, partition_col="date")
# %%
