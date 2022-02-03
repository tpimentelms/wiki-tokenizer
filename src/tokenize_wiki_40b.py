# -*- coding: utf-8 -*-
import argparse
import re
import math
from tqdm import tqdm
import tensorflow as tf
import tensorflow_datasets as tfds

from tokenize_wiki_latest import get_tokenizer, get_sentencizer, tokenize_sentence, write_txt

r1 = "_START_ARTICLE_\n[^_]*"
r2 = "_START_PARAGRAPH_\n"
r3 = "_START_SECTION_\n[^_]*"
r4 = "_NEWLINE_"

ARTICLE_REGEX = re.compile(f"({r1}|{r2}|{r3}|{r4})")


def get_args():
    parser = argparse.ArgumentParser()
    # Wikipedia
    parser.add_argument(
        "--raw-data-dir", type=str,
        help="The file containing the wiki json files from which to read")
    parser.add_argument(
        "--tokenized-file", type=str,
        help="The file containing the wiki json files from which to read")
    parser.add_argument(
        "--language", type=str, required=True,
        help="The wikipedia language to get tokenizer.")
    parser.add_argument("--batch-size", type=int, default=1024)
    # parser.add_argument("--data_dir", help="path to save data files to")

    return parser.parse_args()


def process_batch(batch, sentencizer, tokenizer, pbar):
    processed_articles = []
    for item in batch.get("text"):
        text = item.decode("UTF-8")
        text_clean = re.sub(ARTICLE_REGEX, "\n", text)
        paragraphs = [paragraph for paragraph in text_clean.split('\n') if paragraph != '']
        sentences_raw = [sentence for paragraph in paragraphs for sentence in sentencizer(paragraph)]

        token_lists = [tokenize_sentence(tokenizer, sentence) for sentence in sentences_raw]
        sentences = '\n'.join(' '.join(sentence) for sentence in token_lists)
        # import ipdb; ipdb.set_trace()

        processed_articles += [sentences]
        pbar.update(1)

    return processed_articles


def process_tf_dataset(ds, ds_size, tgt_fname, sentencizer, tokenizer):
    # import ipdb; ipdb.set_trace()
    with tqdm(total=ds_size, desc='Getting wiki40b dataset', mininterval=1) as pbar:
        for batch in ds.as_numpy_iterator():
            processed_articles = process_batch(batch, sentencizer, tokenizer, pbar)
            write_txt(tgt_fname, processed_articles)


def get_data(language, raw_data_dir, tgt_fname, batch_size, allow_multilingual=False):
    sentencizer = get_sentencizer(language, allow_multilingual)
    tokenizer = get_tokenizer(language, allow_multilingual)

    for data_split in ['train', 'validation', 'test']:
        # Download the dataset from tensorflow
        ds, ds_info = tfds.load(f"wiki40b/{language}", split=data_split, data_dir=raw_data_dir,
                       shuffle_files=False, batch_size=batch_size, with_info=True)
        ds_size = ds_info.splits[data_split].num_examples
        process_tf_dataset(ds, ds_size, tgt_fname, sentencizer=sentencizer, tokenizer=tokenizer)


def main():
    args = get_args()
    print(args)

    get_data(args.language, raw_data_dir=args.raw_data_dir,
             tgt_fname=args.tokenized_file, batch_size=args.batch_size)


if __name__ == '__main__':
    main()
