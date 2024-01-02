from writing.wiki_manager import WikiManager


def suggest_art_for_articles(wiki: WikiManager):
    """
    Suggests art for articles.
    """
    # Iterate over all the articles
    for article in wiki.articles:
        # Iterate over the sections in the article, where each section is started by a line that starts with a "#"
        sections = article.get_sections()
        for section_name, section_content in sections:
            pass