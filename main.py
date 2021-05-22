import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import string

WHITELIST_MARKDOWNS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']
WEBSITES = ["http://he.wikipedia.org",
            "http://ynet.co.il",
            "http://www.talniri.co.il"]
MINIMUM_WORD_LEN = 2


def remove_punctuation(word):
    for punctuation in string.punctuation:
        word = word.replace(punctuation, '')
    return word


def remove_digits(word):
    for digit in range(10):
        word = word.replace(str(digit), '')
    return word


def extract_text_from_websites(websites):
    """
    Extract text from HTML and merge to a global text field
    """
    global_text_pool = ''
    for url in websites:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        text = ' '.join([' '.join(s.findAll(text=True)) for s in soup.findAll(WHITELIST_MARKDOWNS)])
        global_text_pool += text
        # Separate different websites while concatenating.
        global_text_pool += ' '
    return global_text_pool


def get_most_common_words_from_text(text):
    """
    Return: most common words per len
    """
    c = Counter([r.strip().lower() for r in text.split()])
    df = pd.DataFrame(c.items(), columns=['word', 'count'])
    df['word'] = df['word'].apply(remove_punctuation)
    df['word'] = df['word'].apply(remove_digits)
    df['len'] = df['word'].str.len()
    df = df.sort_values(['len', 'count'], ascending=[True, False])
    df = df[df['len'] >= MINIMUM_WORD_LEN]
    top_words_by_len = df.groupby('len').first()
    return top_words_by_len


def print_words_by_len(top_words_by_len):
    """
    Print the DataFrame with the following format:
    len: word
    """
    print(f'{top_words_by_len.index}: {top_words_by_len["word"]}')


if __name__ == '__main__':
    text = extract_text_from_websites(WEBSITES)
    top_words_by_len = get_most_common_words_from_text(text)
    print_words_by_len(top_words_by_len)
