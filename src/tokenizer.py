import spacy


class Tokenizer:

    def __init__(self, language):
        self.language = language
        self.tokenizer = self.get_tokenizer(language)

    @classmethod
    def get_tokenizer(cls, language):
        nlp = spacy.blank(language)
        spacy_tokenizer = nlp.Defaults.create_tokenizer(nlp)
        return spacy_tokenizer

    def __call__(self, *args, **kwargs):
        return self.tokenizer(*args, **kwargs)
