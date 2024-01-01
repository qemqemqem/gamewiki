import math

from writing.wiki_manager import WikiManager

# Do this at load time, because it's slow
print("Loading list of words...")
with open("data/en_gt_100.txt", 'r') as f:
    list_of_words = f.read().splitlines()
list_of_words = [line.split(" ")[0].lower() for line in list_of_words if " " in line]


def find_penalty_for_article_commonality(wiki: WikiManager, article_name: str) -> float:
    if article_name.lower() not in list_of_words:
        return 0
    index = list_of_words.index(article_name.lower())
    penalty = -1 * math.log10(index)
    # Words like "elves" are about -3 penalty with just a base10, might want to multiply by 2 or 3 or something
    return penalty


def select_next_article(wiki: WikiManager) -> str:
    # Get all links
    links = wiki.get_all_links()

    # Sort links by count
    links = {k: v for k, v in sorted(links.items(), key=lambda item: item[1], reverse=False)}

    # Print all links
    for link, count in links.items():
        print(f"{link} ({count})")

    # Score each article
    scores = {}
    for link, count in links.items():
        scores[link] = count + find_penalty_for_article_commonality(wiki, link)

    # TODO: Revisit existing articles that need updating

    # Remove articles that already exist
    for article in wiki.articles:
        if article.title in scores:
            del scores[article.title]

    # Return highest scoring article name
    best = max(scores, key=scores.get)
    return best