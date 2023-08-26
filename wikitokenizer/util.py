# -*- coding: utf-8 -*-
import os
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
