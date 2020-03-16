# import spacy
from .spacy_base import SpacyBase


class Sentencizer(SpacyBase):

    def get_model(self, language):
        nlp = self.get_spacy_nlp(language)
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        self.sentencizer = nlp

    def __call__(self, *args, **kwargs):
        return [x.text for x in self.sentencizer(*args, **kwargs).sents]
