# wiki-tokenizer

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

### Usage

To download and tokenize wikipedia data for a specific language do:
```bash
$ make LANGUAGE=<wikipedia-language-code>
```
Where `<wikipedia-language-code>` is the language code in wikipedia for the desired language. To tokenize Afrikaans data, for example, run:
```bash
$ make LANGUAGE=af
```
