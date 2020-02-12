# wiki-tokenizer

Code to download and tokenize wikipedia data.

### Installation

You can install the tokenizer directly from PyPI:

`pip install token-wiki`

Or from source:

```
git clone https://github.com/tiagopms/wiki-tokenizer.git
cd wiki-tokenizer
pip install .
```

#### Dependencies

Wiki tokenizer has the following requirements:

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
