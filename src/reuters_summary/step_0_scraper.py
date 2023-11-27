import datetime
from dataclasses import asdict, dataclass, field

import newspaper
import pandas as pd
import requests
from bs4 import BeautifulSoup


@dataclass
class WorldArea:
    area: str
    base_url: str
    number_of_articles_to_fetch: int
    articles_links: list[str] = field(default_factory=list)
    articles_text: list[str] = field(default_factory=list)


@dataclass
class NewsArticle:
    title: str
    text: str


def scrape_articles(
    areas_to_fetch: list[str],
    reuters_url: str,
    number_articles_to_fetch: int,
) -> pd.DataFrame:
    """_summary_

    Args:
        areas_to_fetch (list[str]): world areas to fetch from reuters site
        reuters_url (str): Base reuters website url.
        number_articles_to_fetch (int): how many articles about to fetch
    Returns:
        pd.DataFrame: dataframe with fetched articles texts
    """
    world_areas_created = _create_world_area_objects(
        areas=areas_to_fetch,
        url=reuters_url,
        number_articles_to_fetch=number_articles_to_fetch,
    )
    world_areas_with_article_urls = [
        _fetch_area_articles_urls(world_area=world_area)
        for world_area in world_areas_created
    ]
    world_areas_with_fetched_articles_text = [
        _save_articles_text(world_area=world_area)
        for world_area in world_areas_with_article_urls
    ]
    articles_df = prepare_fetched_articles_for_saving(
        articles_text=world_areas_with_fetched_articles_text
    )
    return articles_df


def prepare_fetched_articles_for_saving(articles_text: list[WorldArea]) -> pd.DataFrame:
    """
    Convert list of fetched articles with metadata to a DataFrame.
    """
    dfs = []
    for area in articles_text:
        df = pd.DataFrame(asdict(area))
        df["title"] = [
            df["articles_text"].values[i]["title"] for i in range(df.shape[0])
        ]
        df["text"] = [df["articles_text"].values[i]["text"] for i in range(df.shape[0])]
        df = df[["area", "articles_links", "title", "text"]].rename(
            {"articles_links": "article_link"}
        )
        dfs.append(df)
    df_to_save = pd.concat(dfs).drop_duplicates(subset="title").reset_index(drop=True)
    df_to_save["date"] = int(datetime.date.today().strftime("%Y%m%d"))
    return df_to_save


def _create_world_area_objects(
    areas: list[str],
    url: str,
    number_articles_to_fetch: int,
) -> list[WorldArea]:
    """
    Create WorldArea object with area names, base_url and number_of_articles_to_fetch.
    Args:
        areas (list[str]): world areas to fetch from reuters site
        url (str): Base reuters website url.
        number_of_world_articles_to_fetch (int): how many articles to fetch

    Returns:
        list[WorldArea]: list of WorldArea objects
    """
    world_areas = []
    for area in areas:
        area_to_fetch = WorldArea(
            area=area,
            base_url=f"{url}/{area}/?date=today",
            number_of_articles_to_fetch=number_articles_to_fetch,
        )
        world_areas.append(area_to_fetch)
    return world_areas


def _fetch_area_articles_urls(world_area: WorldArea) -> WorldArea:
    """
    For each world_area get list of article urls to download.
    """
    response = requests.get(world_area.base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links_with_class = soup.find_all("div", class_="story-content")
    links = []
    for link in links_with_class[: world_area.number_of_articles_to_fetch]:
        full_url = f"https://www.reuters.com{link.a['href']}"
        links.append(full_url)
    setattr(world_area, "articles_links", links)
    return world_area


def _fetch_article_text(article_url: str) -> NewsArticle:
    """
    Fetch text of one article
    """
    article = newspaper.Article(article_url)
    article.download()
    article.parse()
    return NewsArticle(title=article.title, text=article.text)


def _save_articles_text(world_area: WorldArea) -> WorldArea:
    """
    For each world area get text of all articles.
    """
    texts = []
    for url in world_area.articles_links:
        text = _fetch_article_text(url)
        texts.append(text)
    setattr(world_area, "articles_text", texts)
    return world_area
