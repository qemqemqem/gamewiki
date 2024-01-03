from pathlib import Path
from typing import List, Optional

from config.globals import LLM_MODEL
from utils.dalle import get_picture_and_download
from utils.gpt import prompt_completion_chat
from writing.article import Article
from writing.wiki_manager import WikiManager

import concurrent.futures
import os
import datetime


def get_description(article: Article) -> str:
    with open("prompts/get_art_description.txt", 'r') as f:
        prompt = f.read()

    prompt = prompt.format(article_wikitext=article.content_wikitext)

    response = prompt_completion_chat(prompt, max_tokens=2048, model=LLM_MODEL)

    return response


def use_description(wiki_name: str, article_file_name: str, description: str) -> str:
    # TODO Process the description
    section = "top"
    prompt = "Cool fantasy art"

    save_loc = f"multiverse/{wiki_name}/images/{article_file_name.title}_S_{section}.png"
    get_picture_and_download(save_loc, prompt)

    # TODO: Add the image to the article

    return save_loc


def fetch_and_save_description(wiki: WikiManager, article: Article) -> Optional[str]:
    try:
        description = get_description(article)
        filename = f"multiverse/{wiki.wiki_name}/art_descriptions/{article.title}.txt"
        with open(filename, 'w') as file:
            file.write(description)
            file.write(f"\n\nRetrieved at: {datetime.datetime.now()}")
            file.write("\nUsed: False")
        return filename
    except Exception as e:
        with open("logging/art_errors.txt", 'a') as error_file:
            error_file.write(f"Error fetching description for {article.title}: {e}\n")
        return None


def process_description(wiki: WikiManager, filename: str) -> None:
    if filename:
        article_title = os.path.basename(filename).split('.txt')[0]
        with open(filename, 'r') as file:
            description = file.read()
        try:
            use_description(wiki.wiki_name, article_title, description)
            # Update the status in the file
            with open(filename, 'a') as file:
                file.write("\nUsed: True")
        except Exception as e:
            with open("logging/art_errors.txt", 'a') as error_file:
                error_file.write(f"Error processing description for {article_title}: {e}\n")

def create_art_for_articles(wiki: WikiManager, max_num_fetch_parallel: int = 1, max_num_process_parallel: int = 1) -> None:
    articles: List[Article] = wiki.articles
    os.makedirs("descriptions", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    # Use separate executors for fetching and processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_num_fetch_parallel) as fetch_executor,\
         concurrent.futures.ThreadPoolExecutor(max_workers=max_num_process_parallel) as process_executor:
        # Submit fetch tasks
        future_to_filename = {fetch_executor.submit(fetch_and_save_description, wiki, article): article for article in articles}

        # Process descriptions as they are fetched
        for future in concurrent.futures.as_completed(future_to_filename):
            article = future_to_filename[future]
            try:
                filename = future.result()
                if filename:
                    # Submit process tasks
                    process_executor.submit(process_description, wiki, filename)
            except Exception as e:
                with open("logging/art_errors.txt", 'a') as error_file:
                    error_file.write(f"Error in fetching description for {article.title}: {e}\n")


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


if __name__ == "__main__":
    wiki_name = "world1"
    wiki_path = Path(f"multiverse/{wiki_name}/wiki/docs")

    # Load all articles
    wiki = WikiManager(wiki_name, wiki_path)

    create_art_for_articles(wiki)
