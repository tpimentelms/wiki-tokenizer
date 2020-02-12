# Process Wikipedia to tokens, tailored to wikipedia-extractor.py dump output
import logging
import json
import argparse
import spacy
from tqdm import tqdm
import gensim.utils


logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)
parser = argparse.ArgumentParser()
# Wikipedia
parser.add_argument(
    "--wikipedia-raw-file", type=str,
    help="The file containing the wiki json files from which to read")
parser.add_argument(
    "--wikipedia-tokenized-file", type=str,
    help="The file in which wikipedia tokenized results should be")
parser.add_argument(
    "--dump-size", type=int, default=1000, required=False,
    help="The number of articles to be processed between each dump")
parser.add_argument(
    "--max-articles", type=int, default=None, required=False,
    help="The maximum number of articles to be processed")
# Model
parser.add_argument(
    "--spacy", default='xx_ent_wiki_sm', required=False,
    help="The name of the spaCy language model (default is multilingual)")


def load_spacy(spacy_option):
    logging.info("Loading spaCy model")
    nlp = spacy.load(spacy_option)
    spacy_tokenizer = nlp.Defaults.create_tokenizer(nlp)
    return spacy_tokenizer


def get_paragraphs(sections):
    paragraphs = [paragraph
                  for section in sections
                  for paragraph in list(filter(None, section.split('\n')))]
    paragraphs = '. '.join(paragraphs)
    paragraphs = paragraphs.replace('\'', '')
    return paragraphs


def get_sentences(article):
    sections = article.get('section_texts')
    paragraphs = get_paragraphs(sections)
    return list(filter(None, paragraphs.split('.')))


def tokenize_sentence(spacy_tokenizer, sentence):
    return [x.text for x in spacy_tokenizer(sentence.strip())]


def process_sentences(sentences, spacy_tokenizer):
    parsed_sentences = []
    for sentence in sentences:
        target_tokens = tokenize_sentence(spacy_tokenizer, sentence)
        if len(target_tokens) > 1:
            parsed_sentences += [' '.join(target_tokens)]

    if len(parsed_sentences) > 10:
        return ' '.join(parsed_sentences)
    else:
        return None


def process_article(article, spacy_tokenizer):
    article = json.loads(article)
    sentences = get_sentences(article)
    parsed = process_sentences(sentences, spacy_tokenizer)
    return parsed


def write_txt(fname, data):
    tqdm.write('Saving dump')
    with open(fname, 'a') as f:
        for item in data:
            f.write("%s\n" % item)


def get_n_articles(src_fname, max_articles=None):
    n_articles = 0
    with gensim.utils.open(src_fname, 'rb') as f:
        for _ in tqdm(f, desc='Getting wikipedia length', mininterval=.2):
            n_articles += 1
            if max_articles is not None and n_articles == max_articles:
                break

    return n_articles


def tokenize_wikipedia(src_fname, tgt_fname, spacy_tokenizer,
                       dump_size, max_articles):
    logging.info('Getting wikipedia number of articles')
    n_articles = get_n_articles(src_fname, max_articles=max_articles)
    processed_articles = []

    logging.info('Preprocessing wikipedia')
    with gensim.utils.open(src_fname, 'rb') as f:
        for article_id, article in tqdm(enumerate(f), total=n_articles, desc='Tokenizing wikipedia', mininterval=.2):
            processed_article = process_article(article, spacy_tokenizer)
            if processed_article is not None:
                processed_articles += [processed_article]

            if ((article_id + 1) % dump_size) == 0:
                write_txt(tgt_fname, processed_articles)
                processed_articles = []

            if max_articles is not None and article_id == max_articles:
                break

    if processed_articles:
        write_txt(tgt_fname, processed_articles)


def process(src_fname, tgt_fname, spacy_option, dump_size, max_articles):
    spacy_tokenizer = load_spacy(spacy_option)

    tokenize_wikipedia(src_fname, tgt_fname, spacy_tokenizer, dump_size, max_articles)
    logging.info("Completed %s, dumped to %s", src_fname, tgt_fname)


def main():
    args = parser.parse_args()
    logging.info(args)

    process(args.wikipedia_raw_file, args.wikipedia_tokenized_file, args.spacy, args.dump_size, args.max_articles)


if __name__ == '__main__':
    main()
