# -*- coding: utf-8 -*-
import argparse
import re
from tqdm import tqdm
import tensorflow_datasets as tfds

from .util import get_tokenizer, get_sentencizer, tokenize_sentence, write_txt

REGEX_1 = "_START_ARTICLE_\n[^_]*"
REGEX_2 = "_START_PARAGRAPH_\n"
REGEX_3 = "_START_SECTION_\n[^_]*"
REGEX_4 = "_NEWLINE_"

ARTICLE_REGEX = re.compile(f"({REGEX_1}|{REGEX_2}|{REGEX_3})")


def get_args():
    parser = argparse.ArgumentParser()
    # Wikipedia
    parser.add_argument(
        "--raw-data-dir", type=str,
        help="The file containing the wiki json files from which to read")
    parser.add_argument(
        "--tgt-dir", type=str, required=True,
        help="The file containing the wiki json files from which to read")
    parser.add_argument(
        "--language", type=str, required=True,
        help="The wikipedia language to get tokenizer.")
    parser.add_argument(
        "--break-text-mode", type=str, default='document',
        choices=['document', 'paragraph', 'sentence'],
        help="Save text in one line per document, paragraph, or sentence.")
    parser.add_argument(
         "--dont-tokenize", action='store_true',
         help="Save data without tokenising the text.")
    parser.add_argument("--batch-size", type=int, default=1024)

    return parser.parse_args()


def process_batch(batch, break_text_mode, sentencizer, tokenizer, pbar):
    processed_articles = []
    for item in batch.get("text"):
        text = item.decode("UTF-8")
        text = re.sub(REGEX_4, " ", text)
        text_clean = re.sub(ARTICLE_REGEX, "\n", text)
        paragraphs = [paragraph for paragraph in text_clean.split('\n') if paragraph.strip() != '']

        if break_text_mode == 'sentence':
            utterances_raw = [
                sentence
                for paragraph in paragraphs
                for sentence in sentencizer(paragraph) if sentence.strip() != ''
            ]
        elif break_text_mode == 'paragraph':
            utterances_raw = paragraphs
        elif break_text_mode == 'document':
            utterances_raw = [' '.join(paragraphs)]
        else:
            raise ValueError(f'Invalid break_text_mode selected {break_text_mode}.')

        token_lists = [tokenize_sentence(tokenizer, utterance) for utterance in utterances_raw]
        utterances = '\n'.join(' '.join(utterance) for utterance in token_lists)

        processed_articles += [utterances]
        pbar.update(1)

    return processed_articles


def process_tf_dataset(dataset, dataset_size, tgt_fname, break_text_mode, sentencizer, tokenizer):
    with tqdm(total=dataset_size, desc='Getting wiki40b dataset', mininterval=1) as pbar:
        for batch in dataset.as_numpy_iterator():
            processed_articles = process_batch(batch, break_text_mode, sentencizer, tokenizer, pbar)
            write_txt(tgt_fname, processed_articles)


def get_data(language, raw_data_dir, tgt_dir, batch_size, break_text_mode,
             allow_multilingual=False, dont_tokenize=False):
    sentencizer = get_sentencizer(language, allow_multilingual)
    tokenizer = None if dont_tokenize else get_tokenizer(language, allow_multilingual)

    for data_split in ['train', 'validation', 'test']:
        # Download the dataset from tensorflow
        dataset, dataset_info = tfds.load(
            f"wiki40b/{language}", split=data_split, data_dir=raw_data_dir,
            shuffle_files=False, batch_size=batch_size, with_info=True)
        dataset_size = dataset_info.splits[data_split].num_examples
        tgt_fname = f'{tgt_dir}/{data_split}.txt'
        process_tf_dataset(
            dataset, dataset_size, tgt_fname, break_text_mode,
            sentencizer=sentencizer, tokenizer=tokenizer)


def main():
    args = get_args()
    print(args)

    get_data(args.language, raw_data_dir=args.raw_data_dir,
             tgt_dir=args.tgt_dir, batch_size=args.batch_size,
             break_text_mode=args.break_text_mode,
             dont_tokenize=args.dont_tokenize)


if __name__ == '__main__':
    main()
