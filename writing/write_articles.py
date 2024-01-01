from pathlib import Path

from strategy.next_article_selection import select_next_article
from writing.wiki_manager import WikiManager


def load_wiki(wiki_name: str = "testing") -> WikiManager:
    wiki_path = Path(f"multiverse/{wiki_name}/wiki/docs")

    # Load all articles
    wiki = WikiManager(wiki_name, wiki_path)

    # Get all links
    links = wiki.get_all_links()

    # Sort links by count
    links = {k: v for k, v in sorted(links.items(), key=lambda item: item[1], reverse=False)}

    # Print all links
    for link, count in links.items():
        print(f"{link} ({count})")

    return wiki

def add_articles_to_wiki(wiki_name: str = "testing", num_new_articles: int = 1):
    wiki_path = Path(f"multiverse/{wiki_name}/wiki/docs")

    for i in range(num_new_articles):
        # Load all articles
        wiki = WikiManager(wiki_name, wiki_path)

        # Select next article
        next_article = select_next_article(wiki)
        print(f"Next article: {next_article}")

        # # Get all links
        # links = wiki.get_all_links()
        #
        # # Sort links by count
        # links = {k: v for k, v in sorted(links.items(), key=lambda item: item[1], reverse=False)}
        #
        # # Print all links
        # for link, count in links.items():
        #     print(f"{link} ({count})")
        #
        # # Add articles to wiki
        # for link, count in links.items():
        #     if count > 1:
        #         wiki.add_article(link)