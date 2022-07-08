# wiki-tokenizer

[![CircleCI](https://circleci.com/gh/tpimentelms/wiki-tokenizer.svg?style=svg)](https://circleci.com/gh/tpimentelms/wiki-tokenizer)

Code to download and tokenize wikipedia data.

## Install

To install dependencies run:
```bash
$ conda env create -f environment.yml
```

#### Dependencies

Wiki tokenizer has the following main requirements:

* [SpacY](https://spacy.io/)
* [Gensim](https://radimrehurek.com/gensim/)
* [TensorFlow](https://www.tensorflow.org/)

### Usage

To download and tokenize wikipedia data for a specific language in [Wiki40B](https://aclanthology.org/2020.lrec-1.297/):
```bash
$ make LANGUAGE=<wikipedia-language-code>
```
Where `<wikipedia-language-code>` is the language code in wikipedia for the desired language. To tokenize Afrikaans data, for example, run:
```bash
$ make LANGUAGE=af
```

To instead download raw dumps directly from Wikipedia, run:
```bash
$ make LANGUAGE=<wikipedia-language-code> IS_WIKI40B=False
```

Finally, to fallback to using multilingual tokenizer / sentencizer models (instead of language specific ones), set `MULTILINGUAL=True` when calling the Makefile.
