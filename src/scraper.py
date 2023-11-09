
import newspaper
import json
import dataclasses
from dataclasses import dataclass, field

BASE_URL = "https://www.reuters.com/world"
WORLD_AREAS_TO_FETCH = ["","africa","americas","asia-pacific","europe","middle-east"]

@dataclass
class WorldArea:
    area:str
    base_url:str
    number_of_articles_to_fetch:int
    articles_links: list[str] = field(default_factory=list)
    articles_text: list[str] = field(default_factory=list)

@dataclass
class NewsArticle:
    title:str
    text:str

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

json.dumps(foo, cls=EnhancedJSONEncoder)


def create_world_area_objects(areas:list[str],url:str = BASE_URL) -> list[WorldArea]:
    """
    Create WorldArea object with area names, base_url and number_of_articles_to_fetch.
    Args:
        areas (list[str]): world areas to fetch from reuters site
        url (str, optional): Base reuters website url. Defaults to BASE_URL.

    Returns:
        list[WorldArea]: list of WorldArea objects
    """
    world_areas= []
    for area in areas:
        if area == "": # world area
            number_articles_to_fetch = 5
        else:
            number_articles_to_fetch = 3
        area_to_fetch = WorldArea(area=area,base_url=f"{url}/{area}", number_of_articles_to_fetch=number_articles_to_fetch)
        world_areas.append(area_to_fetch)
    return world_areas

def fetch_area_articles_urls(world_area:WorldArea) -> WorldArea:
    """
    For each world_area get list of article urls to download.
    """
    area_articles_website = newspaper.build(world_area.base_url,language="en", memoize_articles=False)
    area_articles_website_to_fetch = area_articles_website.articles
    area_articles_website_to_fetch = [article.url for article in area_articles_website_to_fetch[:world_area.number_of_articles_to_fetch]]
    setattr(world_area,"articles_links",area_articles_website_to_fetch)
    return world_area


def _fetch_article_text(article_url:str)->str:
    """
    Fetch text of one article
    """
    article = newspaper.Article(article_url)
    article.download()
    article.parse()
    return NewsArticle(title=article.title,text = article.text)

def fetch_articles_text(world_area:WorldArea) -> WorldArea:
    """
    For each world area get text of all articles.
    """
    texts = []
    for url in world_area.articles_links:
        text = _fetch_article_text(url)
        texts.append(text)
    setattr(world_area,"articles_text",texts)
    return world_area



world_areas = create_world_area_objects(areas=WORLD_AREAS_TO_FETCH)
world_areas = [fetch_area_articles_urls(world_area=world_area) for world_area in world_areas]
world_areas = [fetch_articles_text(world_area=world_area) for world_area in world_areas]
