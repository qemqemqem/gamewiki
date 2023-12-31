import re


# Formatting notes:
# - Names cannot have square brackets in them, because of the '[^\]]' regex pattern


def sanitize_article_name(article_name: str) -> str:
    # In standard URLs, a comma is typically encoded as %2C. Use regex to do this replacement
    article_name = re.sub(r",", "%2C", article_name)
    return article_name


def reverse_sanitize_article_name(article_name: str) -> str:
    # Convert "%2C" back to a comma
    article_name = re.sub(r"%2C", ",", article_name)
    return article_name


def convert_markdown_to_wikitext_links(markdown_text: str) -> str:
    # Use regular expressions to find all [text](link) patterns, and replace them with [[link|text]] or just [[link]] if text==link
    t = markdown_text
    t = re.sub(r"\[([^\]]*?)\]\(([^\]]*?)\.md\)", r"[[\2|\1]]", t)

    # Find all links like [[\1|\1]] and replace them with just [[\1]], but only in cases where the text before and after the '|' are the same
    pipe_links = re.findall(r"\[\[([^\]]*?)\|([^\]]*?)\]\]", t)
    for pl in pipe_links:
        if pl[0] == sanitize_article_name(pl[1]):
            t = t.replace(f"[[{pl[0]}|{pl[1]}]]", f"[[{reverse_sanitize_article_name(pl[0])}]]")

    return t


def convert_wikitext_to_markdown_links(wikitext: str) -> str:
    t = wikitext

    # Use regular expressions to convert [[link|text]] to [text](link)
    t = re.sub(r"\[\[([^\]]*?)\|([^\]]*?)\]\]", r"[\2](\1.md)", t)

    # Use regular expressions to convert [[link]] to [link](link)
    t = re.sub(r"\[\[(.*?)\]\]", r"[\1](\1.md)", t)

    # Find all article names and sanitize them, replacing them with the sanitized version
    article_names = re.findall(r"\[(.*?)\]\(.*?\)", t)
    for article_name in article_names:
        if "," in article_name:
            print("Comma!")
        sanitized_name = sanitize_article_name(article_name)
        t = t.replace(f"[{article_name}]({article_name}.md)", f"[{article_name}]({sanitized_name}.md)")

    return t
