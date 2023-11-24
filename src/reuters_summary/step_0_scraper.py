from dataclasses import dataclass, field

import newspaper
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
    number_of_world_articles_to_fetch: int,
    number_of_other_articles_to_fetch: int,
) -> list[WorldArea]:
    """_summary_

    Args:
        areas_to_fetch (list[str]): world areas to fetch from reuters site
        reuters_url (str): Base reuters website url.
        number_of_world_articles_to_fetch (int): how many articles about world data to fetch
        number_of_other_articles_to_fetch (int): how many articles about certain continents to fetch
    Returns:
        list[WorldArea]: list of WorldArea objects
    """
    world_areas_created = _create_world_area_objects(
        areas=areas_to_fetch,
        url=reuters_url,
        number_of_world_articles_to_fetch=number_of_world_articles_to_fetch,
        number_of_other_articles_to_fetch=number_of_other_articles_to_fetch,
    )
    world_areas_with_article_urls = [
        _fetch_area_articles_urls(world_area=world_area)
        for world_area in world_areas_created
    ]
    world_areas_with_fetched_articles_text = [
        _fetch_articles_text(world_area=world_area)
        for world_area in world_areas_with_article_urls
    ]
    return world_areas_with_fetched_articles_text


def _create_world_area_objects(
    areas: list[str],
    url: str,
    number_of_world_articles_to_fetch: int,
    number_of_other_articles_to_fetch: int,
) -> list[WorldArea]:
    """
    Create WorldArea object with area names, base_url and number_of_articles_to_fetch.
    Args:
        areas (list[str]): world areas to fetch from reuters site
        url (str): Base reuters website url.
        number_of_world_articles_to_fetch (int): how many articles about world data to fetch
        number_of_other_articles_to_fetch (int): how many articles about certain continents to fetch

    Returns:
        list[WorldArea]: list of WorldArea objects
    """
    world_areas = []
    for area in areas:
        if area == "world":  # world area
            number_articles_to_fetch = number_of_world_articles_to_fetch
        else:
            number_articles_to_fetch = number_of_other_articles_to_fetch
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


def _fetch_articles_text(world_area: WorldArea) -> WorldArea:
    """
    For each world area get text of all articles.
    """
    texts = []
    for url in world_area.articles_links:
        text = _fetch_article_text(url)
        texts.append(text)
    setattr(world_area, "articles_text", texts)
    return world_area
