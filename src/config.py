from pathlib import Path


class Config:
    REUTERS_URL = "https://www.reuters.com/news/archive"
    WORLD_AREAS_TO_FETCH = [
        "world",
        "africa",
        "usa",
        "asia",
        "europe",
        "middle-east",
    ]
    NUMBER_ARTICLES_TO_FETCH = 10
    RAW_DATA_PATH = Path("./data/raw/raw_articles.parquet")
    SUMMARISED_DATA_PATH = Path("./data/processed/summarised_articles.parquet")
