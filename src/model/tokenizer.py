from .spacy_base import SpacyBase


class Tokenizer(SpacyBase):

    def get_model(self, language):
        nlp = self.get_spacy_nlp(language)
        self.tokenizer = nlp.Defaults.create_tokenizer(nlp)

    def __call__(self, *args, **kwargs):
        return self.tokenizer(*args, **kwargs)
