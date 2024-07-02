# -*- coding: utf-8 -*-
import argparse
from tqdm import tqdm

from .util import get_tokenizer, get_sentencizer, tokenize_sentence, write_txt


def get_args():
    parser = argparse.ArgumentParser()
    # Wikipedia
    parser.add_argument(
        "--src-fname", type=str,
        help="The file containing the wiki json files from which to read")
    parser.add_argument(
        "--tgt-fname", type=str, required=True,
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
    for line in batch:
        paragraph = line.strip()

        if break_text_mode == 'sentence':
            utterances_raw = [
                sentence
                for sentence in sentencizer(paragraph) if sentence.strip() != ''
            ]
        elif break_text_mode in {'paragraph', 'document'}:
            utterances_raw = [paragraph]
        else:
            raise ValueError(f'Invalid break_text_mode selected {break_text_mode}.')

        token_lists = [tokenize_sentence(tokenizer, utterance) for utterance in utterances_raw]
        utterances = '\n'.join(' '.join(utterance) for utterance in token_lists)

        processed_articles += [utterances]
        pbar.update(1)

    return processed_articles


def batch_file_lines(f, batch_size):
    batch = []
    for line in f:
        batch += [line]
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch


def process_file(src_fname, tgt_fname, batch_size, break_text_mode,
                 sentencizer, tokenizer):
    with open(src_fname, 'r', encoding='utf-8') as f:
        with tqdm(desc='Tokenizing file', mininterval=1) as pbar:
            for batch in batch_file_lines(f, batch_size):
                processed_articles = process_batch(
                    batch, break_text_mode, sentencizer, tokenizer, pbar)
                write_txt(tgt_fname, processed_articles)


def tokenize_data(language, src_fname, tgt_fname, batch_size, break_text_mode,
                  allow_multilingual=False, dont_tokenize=False):
    sentencizer = get_sentencizer(language, allow_multilingual)
    tokenizer = None if dont_tokenize else get_tokenizer(language, allow_multilingual)

    process_file(src_fname, tgt_fname, batch_size, break_text_mode,
                 sentencizer=sentencizer, tokenizer=tokenizer)


def main():
    args = get_args()
    print(args)

    tokenize_data(args.language, src_fname=args.src_fname, tgt_fname=args.tgt_fname,
                  batch_size=args.batch_size, break_text_mode=args.break_text_mode,
                  dont_tokenize=args.dont_tokenize)


if __name__ == '__main__':
    main()
