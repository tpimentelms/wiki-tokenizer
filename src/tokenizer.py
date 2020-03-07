import spacy


class Tokenizer:
    spacy_dict = {
        'no': 'nb',  # Norwegian (Bokmål) has a different code in spacy
    }

    def __init__(self, language):
        self.language = language
        self.spacy_language = self.spacy_dict.get(language, language)
        self.tokenizer = self.get_tokenizer(self.spacy_language)

    @classmethod
    def get_tokenizer(cls, language):
        nlp = spacy.blank(language)
        spacy_tokenizer = nlp.Defaults.create_tokenizer(nlp)
        return spacy_tokenizer

    def __call__(self, *args, **kwargs):
        return self.tokenizer(*args, **kwargs)
