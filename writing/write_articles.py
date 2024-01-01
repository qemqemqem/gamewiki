from pathlib import Path

from config.globals import LLM_MODEL
from strategy.next_article_selection import select_next_article
from utils.gpt import prompt_completion_chat
from writing.wiki_manager import WikiManager


def get_article_text(next_article_name: str, wiki: WikiManager) -> str:
    snippets = wiki.get_snippets_that_mention(next_article_name)
    snippets_text = ""
    for article_name, article_snippets in snippets.items():
        for snippet in article_snippets:
            snippets_text += f"The *{article_name}* article says: "
            snippets_text += f"{snippet}\n\n"

    with open("prompts/write_new_article.txt", 'r') as f:
        prompt = f.read()

    prompt = prompt.format(topic=next_article_name, snippets=snippets_text.strip())

    response = prompt_completion_chat(prompt, max_tokens=2048, model=LLM_MODEL)

    return response


def add_articles_to_wiki(wiki_name: str = "testing", num_new_articles: int = 1):
    wiki_path = Path(f"multiverse/{wiki_name}/wiki/docs")

    for i in range(num_new_articles):
        # Load all articles
        wiki = WikiManager(wiki_name, wiki_path)

        # Select next article
        next_article = select_next_article(wiki)
        print(f"Next article: {next_article}")

        # Get article text
        article_text = get_article_text(next_article, wiki)
