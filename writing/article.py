import re
from typing import List, Optional

from formatting.formatting import convert_markdown_to_wikitext_links, convert_wikitext_to_markdown_links, \
    custom_title_case


class Article:
    def __init__(self, title: str, content_markdown: Optional[str] = None, content_wikitext: Optional[str] = None):
        self.title = custom_title_case(title)

        if content_markdown is None and content_wikitext is None:
            raise Exception("Must provide either content_markdown or content_wikitext.")
        elif content_markdown is not None and content_wikitext is None:
            self.content_markdown = content_markdown
            self.content_wikitext = convert_markdown_to_wikitext_links(content_markdown)
        elif content_markdown is None and content_wikitext is not None:
            self.content_wikitext = content_wikitext
            self.content_markdown = convert_wikitext_to_markdown_links(content_wikitext)
        elif content_markdown is not None and content_wikitext is not None:
            raise Exception("Cannot provide both content_wikitext and content_markdown.")

    def get_content_with_wikitext_links(self):
        return self.content_wikitext

    def get_content_with_markdown_links(self):
        return self.content_markdown

    def __str__(self):
        return f"{self.title}"

    def get_all_links(self) -> List[str]:
        links: List[str] = []

        # Use regular expressions to find all [[link|text]] and [[link]] patterns
        # links += re.findall(r"\[\[(.*?)\|(.*?)\]\]", self.content_wikitext)
        links += re.findall(r"\[\[(.*?)\]\]", self.content_wikitext)

        # Find all links with a '|' in them, and replace them with only the second part
        pipe_links = [l for l in links if "|" in l]
        links = [l for l in links if l not in pipe_links]
        # for pl in pipe_links:
        #     links.append()
        links.extend([l.split("|")[0] for l in pipe_links])

        return links

    def get_snippets_that_mention(self, article_name: str) -> List[str]:
        """
        Returns a list of snippets that mention the given article name, where each snippet is a paragraph.
        """
        snippets: List[str] = []

        # Split the content into paragraphs
        paragraphs = self.content_wikitext.split("\n\n")

        # Find all paragraphs that mention the article name
        for paragraph in paragraphs:
            if article_name in paragraph:
                snippets.append(paragraph)

        return snippets
