# Makes programs, downloads sample data, trains a GloVe model, and then evaluates it.
LANGUAGE := af
INPUT_DIR := input
OUTPUT_DIR := output
MULTILINGUAL := False
DUMP_SIZE := 10000
IS_WIKI40B := True

MULTILINGUAL_ARG := $(if $(filter-out $(MULTILINGUAL), False),--allow-multilingual,)

TRUE_STR := True TRUE true
# WIKI40B_LANGUAGES := en ar zh zh-cn zh-tw nl fr de it ja ko pl pt ru es th tr bg ca cs da el et fa fi he hi hr hu id lt lv ms no ro sk sl sr sv tl uk vi
# WIKI_NAME := $(if $(filter $(LANGUAGE),$(WIKI40B_LANGUAGES)),wiki40,latest)

INPUT_DIR_LANG := $(INPUT_DIR)/$(LANGUAGE)
OUTPUT_DIR_LANG := $(OUTPUT_DIR)/$(LANGUAGE)

XML_NAME := $(LANGUAGE)wiki-latest-pages-articles.xml.bz2
WIKIURL := https://dumps.wikimedia.org/$(LANGUAGE)wiki/latest/$(XML_NAME)
JSON_NAME := wiki-latest.json.gz


# Raw Wiki Data Files
XML_FILE := $(INPUT_DIR_LANG)/$(XML_NAME)
JSON_FILE := $(INPUT_DIR_LANG)/$(JSON_NAME)
WIKI_LATEST_FILE := $(OUTPUT_DIR_LANG)/parsed-latest.txt

# Wiki40B Data Files
WIKI40B_FILE := $(OUTPUT_DIR_LANG)/parsed-wiki40b.txt

# Output File
WIKI_FILE := $(if $(filter $(IS_WIKI40B),$(TRUE_STR)),$(WIKI40B_FILE),$(WIKI_LATEST_FILE))


all: get_tokenised

ifneq ($(filter $(IS_WIKI40B),$(TRUE_STR)),)
get_tokenised: $(WIKI40B_FILE)
else
get_tokenised: $(WIKI_LATEST_FILE)
endif

get_data: $(JSON_FILE)

download_raw: $(XML_FILE)



# Tokenize wiki40b
$(WIKI40B_FILE):
	echo "Download data"
	mkdir -p $(OUTPUT_DIR_LANG)
	python src/tokenize_wiki_40b.py --language $(LANGUAGE) --raw-data-dir $(INPUT_DIR_LANG) --tokenized-file $(WIKI40B_FILE)

# Tokenize wikipedia latest
$(WIKI_LATEST_FILE): $(JSON_FILE)
	echo "Tokenize data"
	mkdir -p $(OUTPUT_DIR_LANG)
	python src/tokenize_wiki_latest.py --json-file $(JSON_FILE) --tokenized-file $(WIKI_LATEST_FILE) \
		--language $(LANGUAGE) --dump-size $(DUMP_SIZE) $(MULTILINGUAL_ARG)

# Preprocess wikipedia to json
$(JSON_FILE): $(XML_FILE)
	echo "Parse to JSON data"
	python -m gensim.scripts.segment_wiki -i -f $(XML_FILE) -o $(JSON_FILE)

# Get wikipedia
$(XML_FILE):
	echo "Get data"
	mkdir -p $(INPUT_DIR_LANG)
	wget -P $(INPUT_DIR_LANG) $(WIKIURL)
