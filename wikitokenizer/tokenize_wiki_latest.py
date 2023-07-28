# -*- coding: utf-8 -*-
# Process Wikipedia to tokens, tailored to wikipedia-extractor.py dump output
import os
import json
import argparse
import re
from tqdm import tqdm
import gensim.utils

from .model import Tokenizer, Sentencizer

SKIPPED_ARTICLES, USED_ARTICLES = 0, 0


def get_args():
    parser = argparse.ArgumentParser()
    # Wikipedia
    parser.add_argument(
        "--raw-file", type=str,
        help="The file containing the wiki json files from which to read")
    parser.add_argument(
        "--tokenized-file", type=str,
        help="The file in which wikipedia tokenized results should be")
    parser.add_argument(
        "--dump-size", type=int, default=1000, required=False,
        help="The number of articles to be processed between each dump")
    parser.add_argument(
        "--max-articles", type=int, default=None, required=False,
        help="The maximum number of articles to be processed")
    # Model
    parser.add_argument(
        "--language", type=str, required=True,
        help="The wikipedia language to get tokenizer.")
    parser.add_argument(
        "--allow-multilingual", action='store_true',
        help="Fallback to multilingual sentencizer / tokenizer" +
        "if language specific is not available.")

    return parser.parse_args()


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


def process_sentences(sentences, spacy_tokenizer):
    # pylint: disable=global-statement
    global SKIPPED_ARTICLES, USED_ARTICLES

    parsed_sentences = []
    for sentence in sentences:
        target_tokens = tokenize_sentence(spacy_tokenizer, sentence)
        if len(target_tokens) > 1:
            parsed_sentences += [' '.join(target_tokens)]

    if len(parsed_sentences) > 10:
        USED_ARTICLES += 1
        return '\n'.join(parsed_sentences)

    SKIPPED_ARTICLES += 1
    return None


def process_article(article, spacy_sentencizer, spacy_tokenizer):
    article = json.loads(article)
    sentences = get_sentences(article, spacy_sentencizer)
    parsed = process_sentences(sentences, spacy_tokenizer)
    return parsed


def write_txt(fname, data):
    tqdm.write(f'Saving dump. Stats: Used {USED_ARTICLES}, Skipped {SKIPPED_ARTICLES}')
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, 'a', encoding='utf-8') as f:
        for item in data:
            f.write(f"{item}\n")


def get_n_articles(src_fname, max_articles=None):
    n_articles = 0
    with gensim.utils.open(src_fname, 'rb') as f:
        for _ in tqdm(f, desc='Getting wikipedia length', mininterval=.2):
            n_articles += 1
            if max_articles is not None and n_articles == max_articles:
                break

    return n_articles


def tokenize_wikipedia(src_fname, tgt_fname, spacy_sentencizer, spacy_tokenizer,
                       dump_size, max_articles):
    n_articles = get_n_articles(src_fname, max_articles=max_articles)
    processed_articles = []

    with gensim.utils.open(src_fname, 'rb') as f:
        for article_id, article in tqdm(enumerate(f), total=n_articles,
                                        desc='Tokenizing wikipedia', mininterval=.2):
            processed_article = process_article(article, spacy_sentencizer, spacy_tokenizer)
            if processed_article is not None:
                processed_articles += [processed_article]

            if ((article_id + 1) % dump_size) == 0:
                write_txt(tgt_fname, processed_articles)
                processed_articles = []

            if max_articles is not None and article_id == max_articles:
                break

    if processed_articles:
        write_txt(tgt_fname, processed_articles)


def process(src_fname, tgt_fname, language, dump_size, max_articles, allow_multilingual):
    spacy_sentencizer = get_sentencizer(language, allow_multilingual)
    spacy_tokenizer = get_tokenizer(language, allow_multilingual)

    tokenize_wikipedia(src_fname, tgt_fname, spacy_sentencizer, spacy_tokenizer,
                       dump_size, max_articles)
    print("Completed %s, dumped to %s", src_fname, tgt_fname)


def main():
    args = get_args()
    print(args)

    process(args.raw_file, args.tokenized_file, args.language, args.dump_size,
            args.max_articles, args.allow_multilingual)


if __name__ == '__main__':
    main()
