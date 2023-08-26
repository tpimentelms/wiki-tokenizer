import os
import re
from tqdm import tqdm

from .model import Tokenizer, Sentencizer


SKIPPED_ARTICLES, USED_ARTICLES = 0, 0


def get_sentencizer(language, allow_multilingual=False):
    print("Loading sentencizer")
    sentencizer = Sentencizer(language, allow_multilingual)
    return sentencizer


def get_tokenizer(language, allow_multilingual=False):
    print("Loading tokenizer")
    tokenizer = Tokenizer(language, allow_multilingual)
    return tokenizer


def remove_regex(regex, sections):
    return [
        re.sub(regex, '\n', section)
        for section in sections
    ]


def remove_lists(sections):
    return remove_regex(r'(?m)^\* .+\n?', sections)


def remove_headers(sections):
    return remove_regex(r'(?m)^===.+===\n?', sections)


def get_paragraphs(sections):
    sections = remove_lists(sections)
    sections = remove_headers(sections)
    paragraphs = [paragraph
                  for section in sections
                  for paragraph in list(filter(None, section.split('\n\n')))
                  if paragraph.strip() != '']
    paragraphs = [x.replace('\'', '').replace('\n', ' ') for x in paragraphs]
    return [x for x in paragraphs if x.strip() != '' and len(x) < Sentencizer.MAX_LEN]


def get_sentences(article, spacy_sentencizer):
    sections = article.get('section_texts')
    paragraphs = get_paragraphs(sections)
    sentences = [sentence for x in paragraphs for sentence in spacy_sentencizer(x)]
    return [x for x in sentences if x.strip() != '']


def tokenize_sentence(spacy_tokenizer, sentence):
    tokens = [x.text for x in spacy_tokenizer(sentence.strip())]
    return [x for x in tokens if x.strip() != '']


def write_txt(fname, data, mode='a'):
    tqdm.write(f'Saving dump. Stats: Used {USED_ARTICLES}, Skipped {SKIPPED_ARTICLES}')
    fdir = os.path.dirname(fname)
    if fdir:
        os.makedirs(fdir, exist_ok=True)
    with open(fname, mode, encoding='utf-8') as f:
        for item in data:
            f.write(f"{item}\n")
