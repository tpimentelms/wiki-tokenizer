# -*- coding: utf-8 -*-
# Process Wikipedia to tokens, tailored to wikipedia-extractor.py dump output
import os
import json
import argparse
import re
from tqdm import tqdm
import gensim.utils

from .util import get_tokenizer, get_sentencizer, tokenize_sentence, write_txt, SKIPPED_ARTICLES, USED_ARTICLES


def get_args():
    parser = argparse.ArgumentParser()
    # Wikipedia
    parser.add_argument(
        "--raw-file", type=str,
        help="The file containing the wiki json files from which to read")
    parser.add_argument(
        "--tgt-fname", type=str,
        help="The directory in which wikipedia tokenized results should be")
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

    process(args.raw_file, args.tgt_fname, args.language, args.dump_size,
            args.max_articles, args.allow_multilingual)


if __name__ == '__main__':
    main()
