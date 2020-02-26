# wiki-tokenizer
Code to download and tokenize wikipedia data.

## Install

To install dependencies run:
```bash
$ conda env create -f environment.yml
```

# Running Code

To tokenize a specific language run:
```bash
$ make LANGUAGE=<language-code>
```
The Makefile will automatically download that wikipedia and tokenize it.
