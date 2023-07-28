# wiki-tokenizer

[![CircleCI](https://circleci.com/gh/tpimentelms/wiki-tokenizer.svg?style=svg)](https://circleci.com/gh/tpimentelms/wiki-tokenizer)

Code to download and tokenize wikipedia data.

### Installation

You can install wikitokenizer directly from PyPI:

`pip install wikitokenizer`

Or from source:

```
git clone https://github.com/tpimentelms/wikitokenizer.git
cd wikitokenizer
pip install --editable .
```

#### Dependencies

Wiki tokenizer has the following main requirements:

* [SpacY](https://spacy.io/)
* [Gensim](https://radimrehurek.com/gensim/)
* [TensorFlow](https://www.tensorflow.org/)

### Usage

To download and tokenize wikipedia data for a specific language in [Wiki40B](https://aclanthology.org/2020.lrec-1.297/):
```bash
$ tokenize_wiki_40b --language <wikipedia-language-code> --tokenized-file <tgt_fname>
```
Where `<wikipedia-language-code>` is the language code in wikipedia for the desired language. To tokenize Finnish data, for example, run:
```bash
$ tokenize_wiki_40b --language fi --tokenized-file output/fi/wiki.txt
```

To instead download raw dumps directly from Wikipedia, run:
```bash
$ tokenize_wiki_latest --language fi --tokenized-file output/fi/wiki.txt
```

Finally, to fallback to using multilingual tokenizer / sentencizer models (instead of language specific ones), pass the flag `--allow-multilingual` when calling these scripts.
