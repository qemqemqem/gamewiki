import os
from pathlib import Path
from typing import List, Dict

from writing.article import Article


class WikiManager:
    def __init__(self, wiki_name: str, wiki_path: Path):
        self.wiki_name: str = wiki_name
        self.wiki_path: Path = wiki_path

        # Load all articles
        self.articles: List[Article] = []
        for article_file in os.listdir(self.wiki_path):
            if article_file.endswith(".md"):
                with open(f"{self.wiki_path}/{article_file}", 'r') as f:
                    article_content = f.read()
                article = Article(article_file.replace("\.md", ""), content_markdown=article_content)
                self.articles.append(article)

    def get_article_by_title(self, title: str) -> Article:
        for article in self.articles:
            if article.title == title:
                return article
        raise Exception(f"Article with title {title} not found.")

    def get_all_links(self) -> Dict[str, int]:
        links: Dict[str, int] = {}
        for article in self.articles:
            for link in article.get_all_links():
                if link in links:
                    links[link] += 1
                else:
                    links[link] = 1
        return links
