# Makes programs, downloads sample data, trains a GloVe model, and then evaluates it.
LANGUAGE := af
INPUT_DIR := input
OUTPUT_DIR := output
MULTILINGUAL := False

MULTILINGUAL_ARG := $(if $(filter-out $(MULTILINGUAL), False),--allow-multilingual,)

INPUT_DIR_LANG := $(INPUT_DIR)/$(LANGUAGE)
OUTPUT_DIR_LANG := $(OUTPUT_DIR)/$(LANGUAGE)

XML_NAME := $(LANGUAGE)wiki-latest-pages-articles.xml.bz2
WIKIURL := https://dumps.wikimedia.org/$(LANGUAGE)wiki/latest/$(XML_NAME)
JSON_NAME := wiki-latest.json.gz

# Data Files
XML_FILE := $(INPUT_DIR_LANG)/$(XML_NAME)
JSON_FILE := $(INPUT_DIR_LANG)/$(JSON_NAME)
WIKI_PARSED_FILE := $(OUTPUT_DIR_LANG)/parsed.txt


all: get_wiki

get_wiki: $(WIKI_PARSED_FILE)

get_raw: $(XML_FILE)

# Tokenize wikipedia
$(WIKI_PARSED_FILE): $(JSON_FILE)
	echo "Tokenize data"
	mkdir -p $(OUTPUT_DIR_LANG)
	python src/get_tokens.py --wikipedia-raw-file $(JSON_FILE) --wikipedia-tokenized-file $(WIKI_PARSED_FILE) --language $(LANGUAGE) --dump-size 10000 $(MULTILINGUAL_ARG)

# Preprocess wikipedia to json
$(JSON_FILE): $(XML_FILE)
	echo "Parse to JSON data"
	python -m gensim.scripts.segment_wiki -i -f $(XML_FILE) -o $(JSON_FILE)

# Get wikipedia
$(XML_FILE):
	echo "Get data"
	mkdir -p $(INPUT_DIR_LANG)
	wget -P $(INPUT_DIR_LANG) $(WIKIURL)
