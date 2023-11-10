from pathlib import Path


class Config:
    REUTERS_URL = "https://www.reuters.com/world"
    WORLD_AREAS_TO_FETCH = [
        "",
        "africa",
        "americas",
        "asia-pacific",
        "europe",
        "middle-east",
    ]
    NUMBER_OF_WORLD_ARTICLES_TO_FETCH = 5
    NUMBER_OF_OTHER_ARTICLES_TO_FETCH = 3
    RAW_DATA_PATH = Path("./data/raw/raw_articles.parquet")
