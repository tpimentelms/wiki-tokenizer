# Makes programs, downloads sample data, trains a GloVe model, and then evaluates it.
LANGUAGE := yo
DATA_DIR :=  data
RESULTS_DIR :=  results

DATA_DIR_LANG := $(DATA_DIR)/$(LANGUAGE)

XML_NAME := $(LANGUAGE)wiki-latest-pages-articles.xml.bz2
WIKIURL := https://dumps.wikimedia.org/$(LANGUAGE)wiki/latest/$(XML_NAME)
JSON_NAME := wiki-latest.json.gz

# Data Files
XML_FILE := $(DATA_DIR_LANG)/$(XML_NAME)
JSON_FILE := $(DATA_DIR_LANG)/$(JSON_NAME)
WIKI_PARSED_FILE := $(DATA_DIR_LANG)/parsed.txt


all: get_wiki

get_wiki: $(WIKI_PARSED_FILE)

# Tokenize wikipedia
$(WIKI_PARSED_FILE): $(JSON_FILE)
	echo "Tokenize data"
	python src/tokenizer.py --wikipedia-raw-file $(JSON_FILE) --wikipedia-tokenized-file $(WIKI_PARSED_FILE) --dump-size 10000

# Preprocess wikipedia to json
$(JSON_FILE): $(XML_FILE)
	echo "Parse to JSON data"
	python -m gensim.scripts.segment_wiki -i -f $(XML_FILE) -o $(JSON_FILE)

# Get wikipedia
$(XML_FILE):
	echo "Get data"
	mkdir -p $(DATA_DIR_LANG)
	wget -P $(DATA_DIR_LANG) $(WIKIURL)
