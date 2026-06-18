import json, os, string
from pathlib import Path
from nltk.stem import PorterStemmer


ROOT_DIR = Path(__file__).resolve().parents[2]


def remove_punctuations(text: str) -> str:
    translate_table = str.maketrans({ch: None for ch in string.punctuation})
    return text.translate(translate_table)


def process_stop_words():
    path = os.path.join(ROOT_DIR, "data/stopwords.txt")
    with open(path, "r") as f:
        stop_words = []
        for word in f.read().splitlines():
            stop_words.append(remove_punctuations(word))
    return stop_words


def load_movies():
    movie_file_path = os.path.join(ROOT_DIR, "data/movies.json")
    with open(movie_file_path, "r") as f:
        movie_file = json.load(f)
    return movie_file


STOP_WORDS = process_stop_words()
MOVIE_FILE = load_movies()
stemmer = PorterStemmer()

def keyword_search(query: str) -> list[str]:
    query = stem_words(remove_stop_words(tokenize_text(remove_punctuations(query.lower()))))
    results = []
    for movie in MOVIE_FILE["movies"]:
        id, title = movie["id"], movie["title"]
        pr_title = "".join(
            stem_words(remove_stop_words(tokenize_text(remove_punctuations(title.lower()))))
        )

        for keyword in query:
            if keyword in pr_title:
                results.append([id, title])
                break

    return sorted(results)


def tokenize_text(text: str):
    return text.split()


def remove_stop_words(texts: list[str]) -> list[str]:
    result = []
    for text in texts:
        if text not in STOP_WORDS:
            result.append(text)

    return result

def stem_words(words : list[str]) -> list[str]:
    return [stemmer.stem(word) for word in words]