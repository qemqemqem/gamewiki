import os
from pathlib import Path

from writing.article import Article
from writing.wiki_manager import WikiManager

def load_wiki():
    wiki_name = "testing"
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


if __name__ == "__main__":
    load_wiki()