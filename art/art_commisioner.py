import time
from pathlib import Path
from threading import Thread
from typing import List, Optional

from config.globals import LLM_MODEL
from utils.dalle import get_picture_and_download
from utils.gpt import prompt_completion_chat
from writing.article import Article
from writing.wiki_manager import WikiManager

import concurrent.futures
import os
import datetime


def description_file_exists(wiki_name: str, article_title: str) -> bool:
    return os.path.isfile(f"multiverse/{wiki_name}/art_descriptions/{article_title}.txt")


def image_file_exists(wiki_name: str, article_title: str, section_name: Optional[str] = None) -> bool:
    if section_name is None:
        return os.path.isfile(f"multiverse/{wiki_name}/images/{article_title}.png") or os.path.isfile(f"multiverse/{wiki_name}/images/{article_title}_S_top.png")
    else:
        return os.path.isfile(f"multiverse/{wiki_name}/images/{article_title}_S_{section_name}.png")


def get_description(article: Article) -> str:
    with open("prompts/get_art_description.txt", 'r') as f:
        prompt = f.read()

    prompt = prompt.format(article_wikitext=article.content_wikitext)

    print(f"Getting description for {article.title}...")

    response = prompt_completion_chat(prompt, max_tokens=2048, model=LLM_MODEL)

    return response


def use_description(wiki_name: str, article_file_name: str, description: str) -> str:
    # TODO Process the description
    section = "top"
    prompt = "Cool fantasy art"

    save_loc = f"multiverse/{wiki_name}/images/{article_file_name}_S_{section}.png"
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
    article_title = os.path.basename(filename).split('.txt')[0]
    with open(filename, 'r') as file:
        description = file.read()
    try:
        print(f"Generating art for {article_title}...")
        use_description(wiki.wiki_name, article_title, description)
        # Update the status in the file
        with open(filename, 'a') as file:
            file.write("\nUsed: True")
    except Exception as e:
        with open("logging/art_errors.txt", 'a') as error_file:
            error_file.write(f"Error processing description for {article_title}: {e}\n")


def fetch_descriptions(wiki: WikiManager, articles: List[Article], executor: concurrent.futures.Executor) -> List[str]:
    filenames = []
    for article in articles:
        if not description_file_exists(wiki.wiki_name, article.title):
            future = executor.submit(fetch_and_save_description, wiki, article)
            filename = future.result()
            if filename:
                filenames.append(filename)
    return filenames


def process_images(wiki: WikiManager, executor: concurrent.futures.Executor, polling_interval: int = 1) -> None:
    processed_articles = set()

    while True:
        description_files = [f for f in os.listdir(f"multiverse/{wiki.wiki_name}/art_descriptions") if f.endswith(".txt")]
        for filename in description_files:
            article_title = filename.split('.txt')[0]
            if article_title not in processed_articles and not image_file_exists(wiki.wiki_name, article_title):
                executor.submit(process_description, wiki, f"multiverse/{wiki.wiki_name}/art_descriptions/{filename}")
                processed_articles.add(article_title)

        time.sleep(polling_interval)  # Wait for a second before checking again

def create_art_for_articles(wiki: WikiManager, max_num_fetch_parallel: int = 1, max_num_process_parallel: int = 1) -> None:
    articles: List[Article] = wiki.articles
    os.makedirs("descriptions", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    # Start processing images in a separate thread
    process_thread = Thread(target=process_images, args=(wiki, concurrent.futures.ThreadPoolExecutor(max_workers=max_num_process_parallel)))
    process_thread.start()

    # Fetch descriptions in the main thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_num_fetch_parallel) as fetch_executor:
        fetch_descriptions(wiki, wiki.articles, fetch_executor)

    process_thread.join()  # Wait for the processing thread to finish

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
